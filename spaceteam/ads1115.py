"""Handles ADS1115 ADC on the I2C bus

the I2C address of the ADS1115 is selected via the address pin:
  grnd: 0x48
  Vdd:  0x49
  SDA:  0x4a
  SCL:  0x4b
"""
import time
import smbus

from utils import *

CONVERSION_REGISTER = 0x00
CONFIG_REGISTER = 0x01
DESIRED_CONFIG = [
    1, # operational status (1 means begin single conversion)
    1, 0, 0,  # conversion reads A0 vs. GND
    0, 0, 1,  # gain over the range from GND to approx. 4V
    0, # single-shot conversion mode
    1, 0, 0,  # sampling rate (128 samples per second)
    0, # COMP_MODE set to traditional comparitor (not used, comparator disabled)
    1, # COMP_POL (ALERT/RDY is asserted high)
    1, # COMP_LAT (not used)
    1, 1, # disable the comparitor
  ]

READ_SELECT = [
    DESIRED_CONFIG[0:1] + [1, 0, 0] + DESIRED_CONFIG[4:],
    DESIRED_CONFIG[0:1] + [1, 0, 1] + DESIRED_CONFIG[4:],
    DESIRED_CONFIG[0:1] + [1, 1, 0] + DESIRED_CONFIG[4:],
    DESIRED_CONFIG[0:1] + [1, 1, 1] + DESIRED_CONFIG[4:],
  ]

class ADS1115(object):
  def __init__(self, address, bus=1):
    self.address = address
    self.bus = bus

    self.i2c = smbus.SMBus(self.bus)

    self.config = list(DESIRED_CONFIG)
    self.write_config()

  def write_config(self):
    """set the controls we want for the rest of our interactions with the chip"""
    # the ADS1115 expects MSB first, but linux's write_word_data writes LSB first
    # lets reverse the bytes
    config_msb = bitlist_to_int(self.config[0:8])
    config_lsb = bitlist_to_int(self.config[8:16])
    config_wire = (config_lsb << 8) + config_msb

    #print "write to register 0x%02x : 0x%04x (%s)" % (CONFIG_REGISTER, config_wire, format(config_wire, "#016b"))
    self.i2c.write_word_data(self.address, CONFIG_REGISTER, config_wire)

  def select_input(self, pin, wait = True):
    """Selects a different pin as input for the conversion

    To get an accurate read, it's recommended to wait one sample interval
    """
    if pin < 0 or pin > 3:
      raise RuntimeError("Input pin must be between 0 and 3")

    self.config[3] = pin & 1
    self.config[2] = (pin >> 1) & 1
    self.write_config()

    if wait:
      time.sleep(1.0 / 128)

  def read(self):
    """reads the data at the conversion register"""
    # linux expects to read LSB first; lets re-arrange the bytes we just got
    data = self.i2c.read_word_data(self.address, CONVERSION_REGISTER)

    # at the current lsb, we have the msb
    data_msb = (data & 127) << 8
    data_lsb = data >> 8
    return data_msb + data_lsb
