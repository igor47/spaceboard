"""Handles ADS1115 ADC on the I2C bus

the I2C address of the ADS1115 is selected via the address pin:
  grnd: 0x48
  Vdd:  0x49
  SDA:  0x4a
  SCL:  0x4b

More info:
  https://cdn-shop.adafruit.com/datasheets/ads1115.pdf
"""
import time

from utils import *

CONVERSION_REGISTER = 0x00
CONFIG_REGISTER = 0x01
DEFAULT_CONFIG = [
    1, # operational status (1 means begin single conversion, used in that mode only)
    1, 0, 0,  # conversion reads A0 vs. GND
    0, 0, 1,  # gain over the range from GND to approx. 4V
    0, # single-shot conversion mode
    1, 0, 0,  # sampling rate (128 samples per second)
    0, # COMP_MODE set to traditional comparitor (not used, comparator disabled)
    1, # COMP_POL (ALERT/RDY is asserted high)
    1, # COMP_LAT (not used)
    1, 1, # disable the comparitor
  ]

SAMPLE_RATES = [8, 16, 32, 64, 128, 250, 475, 860]
DEFAULT_SAMPLE_RATE = 128

class ADS1115(object):
  def __init__(self, smbus, address, sps = DEFAULT_SAMPLE_RATE):
    self.smbus = smbus
    self.address = address
    self.samples_per_second = sps

    # store I/O config
    self.pins_enabled = [False] * 4
    self.pin_values = [None] * 4

    self.last_pin_enabled = None

  def __str__(self):
    return "<ADS1115 at {:x}>".format(self.address)

  def communicate(self):
    """Reads the state of all enabled pins and saves it locally"""
    self._read_inputs()

  def _read_inputs(self):
    """reads all enabled pins and stores the values locally"""
    for pin, is_enabled in enumerate(self.pins_enabled):
      if not is_enabled:
        continue

      if pin != self.last_pin_enabled:
        self._write_config(pin)
        # give the device time to read the given input
        time.sleep(1.0 / self.samples_per_second)

        # save the pin we used
        self.last_pin_enabled = pin

      # store the (raw) value into the local register
      self.pin_values[pin] = self._read_value()

  def read(self, pin, scaled = False):
    """returns ; scaled returns values from 0 to 100"""
    value = self.pin_values[pin]

    # something went wrong!
    if value is None:
      if self.pins_enabled[pin]:
        raise RuntimeError(
            "Tried to read pin %s, but it's state is not available!" % pin)
      else:
        raise RuntimeError(
            "Tried to read pin %s, but that pin is not enabled for reading!" % pin)

    # return the value
    else:
      return (float(value) / 0x7FFF * 100) if scaled else value

  def enable_pin(self, pin):
    """enables reading a given pin whenever we read all the inputs"""
    if pin < 0 or pin > 3:
      raise RuntimeError("Input pin must be between 0 and 3, not %s" % pin)

    self.pins_enabled[pin] = True

  def reset(self):
    """reset; really, this just means writing a config"""
    self._write_config()

  @retry_i2c
  def _write_config(self, enabled_pin = 0):
    """set the controls we want for the rest of our interactions with the chip"""
    # lets make a copy of the default config
    config = list(DEFAULT_CONFIG)

    # set the pin we're reading from
    config[2] = (enabled_pin >> 1) & 1
    config[3] = (enabled_pin >> 0) & 1

    # set samples per second
    sps_value = SAMPLE_RATES.index(self.samples_per_second)
    config[6] = (sps_value >> 2) & 1
    config[7] = (sps_value >> 1) & 1
    config[8] = (sps_value >> 0) & 1

    # the ADS1115 expects MSB first, but linux's write_word_data writes LSB first
    # lets reverse the bytes
    config_msb = bitlist_to_int(config[0:8])
    config_lsb = bitlist_to_int(config[8:16])
    config_wire = (config_lsb << 8) + config_msb

    #print "write to register 0x%02x : 0x%04x (%s)" % (CONFIG_REGISTER, config_wire, format(config_wire, "#016b"))
    self.smbus.write_word_data(self.address, CONFIG_REGISTER, config_wire)

  @retry_i2c
  def _read_value(self):
    """reads the raw value of the conversion register"""
    # perform the read via smbus
    data = self.smbus.read_word_data(self.address, CONVERSION_REGISTER)

    # linux expects to read LSB first; lets re-arrange the bytes we just got
    # at the current lsb, we have the msb
    data_msb = (data & 127) << 8
    data_lsb = data >> 8
    value = data_msb + data_lsb

    return value
