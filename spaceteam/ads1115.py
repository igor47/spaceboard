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
import smbus

from utils import *

CONVERSION_REGISTER = 0x00
CONFIG_REGISTER = 0x01
DESIRED_CONFIG = [
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

class ADS1115(object):
  def __init__(self, address, bus=1):
    self.address = address
    self.bus = bus

    self.i2c = smbus.SMBus(self.bus)

    self.config = list(DESIRED_CONFIG)
    self.samples_per_second = 128

    self.select_input(0)

  def write_config(self):
    """set the controls we want for the rest of our interactions with the chip"""
    # set samples per second
    sps_value = SAMPLE_RATES.index(self.samples_per_second)
    self.config[6] = (sps_value >> 2) & 1
    self.config[7] = (sps_value >> 1) & 1
    self.config[8] = (sps_value >> 0) & 1

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

    self.config[2] = (pin >> 1) & 1
    self.config[3] = (pin >> 0) & 1
    self.write_config()

    if wait:
      time.sleep(1.0 / self.samples_per_second)

  def read(self, scaled = False):
    """reads the data at the conversion register; scaled returns values from 0 to 100"""
    # linux expects to read LSB first; lets re-arrange the bytes we just got
    data = self.i2c.read_word_data(self.address, CONVERSION_REGISTER)

    # at the current lsb, we have the msb
    data_msb = (data & 127) << 8
    data_lsb = data >> 8
    value = data_msb + data_lsb

    return (float(value) / 0xFFFF * 100) if scaled else value
