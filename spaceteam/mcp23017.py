"""Handles MCP23017 I/O Expanders on the I2C bus"""
import smbus

ACCEPTABLE_BITS = [0, 1]

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



def bitlist_to_int(bitlist):
  out = 0
  for bit in bitlist:
    if not bit in ACCEPTABLE_BITS:
      raise RuntimeError("bit %s in bitlist %s is not valid!" % (bit, bitlist))

    out = (out << 1) | bit

  return out

class MCP23017(object):
  def __init__(self, address, bus=1):
    self.address = address
    self.bus = bus

    self.i2c = smbus.SMBus(self.bus)
    self.inputs = [1] * 16
    self.output_latches = [0] * 16

    self.set_iocon()
    self.set_pin_modes()

  def write(self, pin, value):
    if self.inputs[pin] != 0:
      raise RuntimeError("Tried to write %s to pin %s, but that pin is an input pin!" % (value, pin))

    if not value in ACCEPTABLE_BITS:
      raise RuntimeError("Value %s (written to MCP at %s pin %s) is not a valid bit" % (value, self.address, pin))

    self.output_latches[pin] = value
    self.write_output_latches()

  def set_as_output(self, pin):
    if self.inputs[pin] != 0:
      self.inputs[pin] = 0
      self.set_pin_modes()

  def set_as_input(self, pin):
    if self.inputs[pin] != 1:
      self.inputs[pin] = 1
      self.set_pin_modes()

  def set_iocon(self):
    """set the controls we want for the rest of our interactions with the chip"""
    self.i2c.write_byte_data(self.address, IOCON_ADDR, bitlist_to_int(DESIRED_IOCON))

  def set_pin_modes(self):
    self.i2c.write_byte_data(self.address, IODIRA_ADDR, bitlist_to_int(self.inputs[0:8]))
    self.i2c.write_byte_data(self.address, IODIRB_ADDR, bitlist_to_int(self.inputs[8:16]))

  def write_output_latches(self):
    self.i2c.write_byte_data(self.address, OLATA_ADDR, bitlist_to_int(self.output_latches[0:8]))
    self.i2c.write_byte_data(self.address, OLATB_ADDR, bitlist_to_int(self.output_latches[8:16]))
    print self.output_latches
