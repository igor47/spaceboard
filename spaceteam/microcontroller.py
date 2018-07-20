#!/usr/bin/python

from cobs import cobs
import io
import select
import serial
import struct
import threading
import time

from colour import Color
from cmdmessenger import CmdMessenger

class Microcontroller(object):
  """interface to an on-board microcontroller"""

  # Timeout for buffered serial I/O in seconds.
  IO_TIMEOUT_SEC = 2

  def __init__(self, port, baud_rate=115200):
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
        timeout=self.IO_TIMEOUT_SEC)
    if not self._serial.isOpen():
      raise ValueError("Couldn't open %s" % port)

    # holds reads until we encounter a 0-byte (COBS!!!)
    self._read_buf = [None] * 256
    self._read_buf_pos = 0

    # How many commands we've sent to the microcontroller.
    self.commands_sent = 0

    # max brightness for the leds
    self.max_brightness = 180

    # do we need to latch the leds?
    self.leds_updated = False

  def stop(self):
    """Shuts down communication to the microcontroller."""
    self._serial.close()

  def _send_command(self, data = []):
    """Sends a command to the microcontroller.

      Args:
          command: An ASCII string which the controller will interpret.

      Returns:
          True if command was sent, False if something went wrong. Note
          this doesn't guarantee the command was actually received.
    """
    encoded = cobs.encode(str(bytearray(data)))
    self._serial.write(encoded + '\x00')

    self.commands_sent += 1
    return True

  def _reset_read_buf(self):
    self._read_buf[0:self._read_buf_pos] = [None] * self._read_buf_pos
    self._read_buf_pos = 0

  def _recv_command(self):
    """Reads a full line from the microcontroller

    We expect to complete a read when this is invoked, so don't invoke unless
    you expect to get data from the microcontroller. we raise a timeout if we
    cannot read a command in the alloted timeout interval."""
    # we rely on the passed-in timeout
    while True:
      c = self._serial.read(1)
      if not c:
        raise serial.SerialTimeoutException(
            "Couldn't recv command in %d seconds" % self.IO_TIMEOUT_SEC)

      # finished reading an entire COBS structure
      if c == '\x00':
        # grab the data and reset the buffer
        data = self._read_buf[0:self._read_buf_pos]
        self._reset_read_buf()

        # return decoded data
        return cobs.decode(str(bytearray(data)))

      # still got reading to do
      else:
        self._read_buf[self._read_buf_pos] = c
        self._read_buf_pos += 1

        # ugh. buffer overflow. wat do?
        if self._read_buf_pos == len(self._read_buf):
          # resetting the buffer likely means the next recv will fail, too (we lost the start bits)
          self._reset_read_buf()
          raise RuntimeError("IO read buffer overflow :(")

  def get_state(self):
    """Updates the internal state with fresh data from the microcontroller"""
    # first, ask for a state update
    self._send_command('G')

    # we expect the microcontroller to respond quickly
    data = self._recv_command()
    if data[0] != 'S' or len(data) != 11:
      raise RuntimeError("Invalid response (with code %s len %d) to a state request" % (data[0]), len(data))

    return {
        'received': struct.unpack('>I', data[1:5]),
        'bad': struct.unpack('>I', data[5:9]),
        'throttle': struct.unpack('>H', data[9:11]),
      }

  def reset(self):
    """Resets the device"""
    self._send_command('R')

  def communicate(self):
    """Performs two-ways comms with peripheral

    In our case, this means syncing the local LED state with the remote LED state"""
    if self.leds_updated:
      self.latch_leds()

  def clear_leds(self):
    """Clears (turns off) all of the leds"""
    self._send_command('C')

  def latch_leds(self):
    """Displays the led values we've sent on the strip"""
    self.leds_updated = False
    self._send_command('L')

  def set_led(self, number, color, latch = False):
    """Sets as specific led to the given color; color is a Colour instance"""
    command = ["O", number] + self.color_to_bit_list(color)
    self._send_command(command)

    self.latch_now_or_later(latch)

  def set_oxygen(self, val):
    """Sets a specific LED in the array"""
    self._send_command(["X", val])

  def update_array(self, bytes):
    """Updates the data displayed by the LED array"""
    self._send_command(['A'] + bytes)

  def set_led_batch(self, first_led, colors = [], latch = False):
    """Sets all specified colors"""
    group_size = 10 # we will set up to 10 leds at once

    while len(colors) > 0:
      current = colors[:group_size]
      color_bytes_lists = [self.color_to_bit_list(c) for c in current]
      color_bytes = [item for sublist in color_bytes_lists for item in sublist]
      command = ["B", first_led] + color_bytes
      self._send_command(command)

      # set up for next loop
      first_led += group_size
      colors = colors[group_size:]

    self.latch_now_or_later(latch)

  def latch_now_or_later(self, latch):
    if latch:
      self.latch_leds()
    else:
      self.leds_updated = True

  def color_to_bit_list(self, color):
    """converts a color into a list of rgb uint8_ts based on max_brightness"""
    return [int(i * self.max_brightness) for i in color.rgb]

if __name__ == "__main__":
  import peripherals
  peripherals.reset_all()

  mic = peripherals.MAPLE

  idx = 0
  while True:
    peripherals.MAPLE.set_led(idx, Color('orange'), latch = True)
    raw_input("turned on %s; press <Enter> to continue..." % idx)

    peripherals.MAPLE.set_led(idx, Color('green'), latch = False)
    idx += 1
