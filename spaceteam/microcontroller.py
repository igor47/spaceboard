#!/usr/bin/python

import copy
import logging
import os
import select
import serial
import threading
import time

class State(object):
  """Represents the microcontroller's current state."""
  def __init__(self,
      timestamp = time.time(),
      commands_sent = 0,
      commands_received = 0,
      bad_commands_received = 0,
      ms_since_command_received = 0,
      ):
    self.timestamp = timestamp
    self.commands_sent = commands_sent
    self.commands_received = commands_received
    self.bad_commands_received = bad_commands_received
    self.ms_since_command_received = ms_since_command_received

  def __repr__(self):
    return "State(timestamp=%f, commands_sent=%d, commands_received=%d, "\
        "bad_commands_received=%d, ms_since_command_received=%d" % (
            self.timestamp,
            self.commands_sent,
            self.commands_received,
            self.bad_commands_received,
            self.ms_since_command_received)

class Microcontroller(object):
  """interface to an on-board microcontroller"""

  # Timeout for buffered serial I/O in seconds.
  IO_TIMEOUT_SEC = 5

  # how stale does the state get until we are considered no longer healthy?
  HEALTH_TIMEOUT = 2

  def __init__(self, port, baud_rate=57600):
    """Connects to the microcontroller on a serial port.

    Args:
        port: The serial port or path to a serial device.
        baud_rate: The bit rate for serial communication.

    Raises:
        ValueError: There is an error opening the port.
        SerialError: There is a configuration error.
    """
    # Build the serial wrapper.
    self._serial = serial.Serial(
        port=port,
        baudrate=baud_rate,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=self.IO_TIMEOUT_SEC, writeTimeout=self.IO_TIMEOUT_SEC)
    if not self._serial.isOpen():
      raise ValueError("Couldn't open %s" % port)

    # container for the internal state
    self.state = None

    # How many commands we've sent to the microcontroller.
    self.commands_sent = 0

    # used to make sure only a single thread tries to write to the microcontroller
    self.write_lock = threading.Lock()

  def stop(self):
    """Shuts down communication to the microcontroller."""
    self._serial.close()

  @property
  def status(self):
    """Returns a dictionary of the microcontroller's status for the client"""
      status = {
          'healthy':self.is_healthy(),
          'sent':self.commands_sent,
          'recieved':self.state.commands_received if self.state else 0,
          'bad':self.state.bad_commands_received if self.state else 0,
          }
      return status

  def _send_command(self, command):
    """Sends a command to the microcontroller.

      Args:
          command: An ASCII string which the controller will interpret.

      Returns:
          True if command was sent, False if something went wrong. Note
          this doesn't guarantee the command was actually received.
    """
    if not acquire(self.write_lock, 2):
      return False

    try:
      self._serial.write(command)
        if not command.endswith('\n'):
          self._serial.write('\n')
        self._serial.flush()
        self.commands_sent += 1
    finally:
      self.write_lock.release()

    return True

  def _read_data(self, timeout = None):
    """Reads a data line from the microcontroller"""
    if timeout is None:
      timeout = self.IO_TIMEOUT_SEC

    line = None

    # Wait for up to timeout seconds for data to become available.
    select.select([self._serial], [], [], timeout)
    if self._serial.inWaiting() != 0:
      line = self._serial.readline().strip()

    return line

  def _parse_data(self, data):
    """Parses the microcontroller raw microcontroller data into meaningful fields

      The microcontroller sends back newline-terminated ascii data.
      Each data line is broken up into fields like so:
          (Field name):(Field data);
      and fields are concatenated together with no spaces
    """
    fields = {}
    for field in data.rstrip(';').split(';'):
      k, v = field.split(':')
        fields[k] = v

    return fields

  def update_state(self, timeout = 0):
    """Updates the internal state with fresh data from the microcontroller"""
    try:
      state_fields = self._parse_data(self._read_data(timeout))
      timestamp = time.time()

      # update the state
      new_state = State(
          timestamp = timestamp,
          commands_sent = self.commands_sent,
          commands_received = int(state['C']),
          bad_commands_received = int(state['B']),
          ms_since_command_received = int(state['L']))
      self.state = new_state

    # failed to parse the state
    except:
      return False
    else:
      return True

  def get_state(self):
    """Returns a copy of the current state."""
    return copy.deepcopy(self.state)
