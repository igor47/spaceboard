"""Abstraction of the RPi"""

import pigpio
import time

RESET_GPIO_BCM = 21

class RPi(object):
  def __init__(self):
    self.pi = pigpio.pi()
    if not self.pi.connected:
      raise RuntimeError("PIGPIOD is not running! Run install.sh")

  def reset_peripherals(self):
    """initiates the reset to bring everything into a default state"""
    self.pi.set_mode(RESET_GPIO_BCM, pigpio.OUTPUT)

    self.pi.write(RESET_GPIO_BCM, 0)
    time.sleep(0.1)
    self.pi.write(RESET_GPIO_BCM, 1)

