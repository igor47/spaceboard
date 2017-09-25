"""Abstraction of the RPi"""

import pigpio
import time

import smbus

RESET_GPIO_BCM = 21
I2C_ALL_CALL = 0x0 # all call address -- goes to all devices (that support it)
I2C_SOFT_RESET = 0x06 # all devices reset

class RPi(object):
  def __init__(self, i2c_bus = 1):
    self.pi = pigpio.pi()
    if not self.pi.connected:
      raise RuntimeError("PIGPIOD is not running! Run install.sh")

    self.i2c_bus = i2c_bus
    self.i2c = smbus.SMBus(self.i2c_bus)

  def reset_peripherals(self):
    """initiates the reset to bring everything into a default state"""
    self.pi.set_mode(RESET_GPIO_BCM, pigpio.OUTPUT)

    self.pi.write(RESET_GPIO_BCM, 0)
    time.sleep(0.1)
    self.pi.write(RESET_GPIO_BCM, 1)

    # issue an i2c general-call reset
    self.i2c.write_byte(I2C_ALL_CALL, I2C_SOFT_RESET)
