"""Handles MCP23017 I/O Expanders on the I2C bus

More info:
  http://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf
"""

from utils import *

import smbus
import time

IOCON_ADDR = 0x0A
DESIRED_IOCON = [
    0, # Bank
    1, # Interrupt Mirror
    0, # Sequential Operations
    0, # Slew rate
    0, # HAEN (N/A for us)
    0, # Interrupt pin mode
    1, # Interrupt means go high
    0, # N/A
  ]

IODIRA_ADDR = 0x00
IODIRB_ADDR = 0x01

GPIOA_ADDR = 0x12
GPIOB_ADDR = 0x13

OLATA_ADDR = 0x14
OLATB_ADDR = 0x15

GPPUA_ADDR = 0x0C
GPPUB_ADDR = 0x0D

class MCP23017(object):
  def __init__(self, smbus, address):
    self.smbus = smbus
    self.address = address

    self.input_latches = [None] * 16

    self.inputs = [1] * 16
    self.mode_changed = False

    self.output_latches = [0] * 16
    self.output_latches_changed = False

  def reset(self):
    """initializes us in a sane configuration"""
    with self.smbus.lock_grabber():
      self._set_iocon()
      self._set_pin_modes()
      self._enable_pullups()
      self._write_output_latches()

  def read(self, pin):
    """returns pin value from inputs"""
    # something went wrong!
    if self.input_latches[pin] is None:
      if not self.inputs[pin]:
        raise RuntimeError(
            "Tried to read pin %s, but that pin is an output pin!" % pin)
      else:
        raise RuntimeError(
            "Tried to read pin %s, but it's state is not available!" % pin)

    # return the value
    else:
      return self.input_latches[pin]

  def write(self, pin, value):
    if self.inputs[pin] != 0:
      raise RuntimeError("Tried to write %s to pin %s, but that pin is an input pin!" % (value, pin))

    if not value in ACCEPTABLE_BITS:
      raise RuntimeError("Value %s (written to MCP at %s pin %s) is not a valid bit" % (value, self.address, pin))

    self.output_latches[pin] = value
    self.output_latches_changed = True

  def communicate(self):
    """Perform two-way comms to sync remote and local state

    This means reading the state of input pins and writing the new
    state of any output pins"""
    # first, perform any writes we need
    if self.mode_changed:
      self._set_pin_modes()
    if self.output_latches_changed:
      self._write_output_latches()

    # next, read the inputs
    self._read_inputs()

  def set_as_output(self, pin):
    if self.inputs[pin] != 0:
      self.inputs[pin] = 0
      self.mode_changed = True

  def set_as_input(self, pin):
    if self.inputs[pin] != 1:
      self.inputs[pin] = 1
      self.mode_changed = True

  def _set_iocon(self):
    """set the controls we want for the rest of our interactions with the chip"""
    self.smbus.write_byte_data(self.address, IOCON_ADDR, bitlist_to_int(DESIRED_IOCON))

  def _set_pin_modes(self):
    """configure pins as either inputs or outputs"""
    self.mode_changed = False
    with self.smbus.lock_grabber():
      self.smbus.write_byte_data(
          self.address,
          IODIRA_ADDR,
          bitlist_to_int(self.inputs[0:8]))
      self.smbus.write_byte_data(
          self.address,
          IODIRB_ADDR,
          bitlist_to_int(self.inputs[8:16]))

  def _write_output_latches(self):
    """for output pins, sets their output value from internal state"""
    self.output_latches_changed = False
    with self.smbus.lock_grabber():
      self.smbus.write_byte_data(
          self.address,
          OLATA_ADDR,
          bitlist_to_int(self.output_latches[0:8]))
      self.smbus.write_byte_data(
          self.address,
          OLATB_ADDR,
          bitlist_to_int(self.output_latches[8:16]))

  def _read_inputs(self):
    """Reads the state of input pins into a local register

    Sets local register to a list of length 16, with states at 0 or 1 for input
    pins or None for output pins"""
    bits = []
    with self.smbus.lock_grabber():
      for port in [GPIOA_ADDR, GPIOB_ADDR]:
        data = self.smbus.read_byte_data(self.address, port)
        port_bits = list(format(data, "08b"))
        bits += port_bits

    # now bits contains 0s and 1s for each input, but we
    # should ignore output pins
    for pin, is_input in enumerate(self.inputs):
      if not is_input:
        bits[pin] = None

    self.input_latches = bits

  def _enable_pullups(self):
    """Enable pull-up resistors on all input pins"""
    self.smbus.write_byte_data(self.address, GPPUA_ADDR, 0xFF)
    self.smbus.write_byte_data(self.address, GPPUB_ADDR, 0xFF)
