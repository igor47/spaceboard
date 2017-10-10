#!/usr/bin/env python2.7
"""
Initializes and provides access to board peripherals
"""

import time

from errors import *

# initialize GPIO
import wiringpi
wiringpi.wiringPiSetup()

RESET_PIN = 29

# initialize I2C using smbus
import smbus
_SMBUS = smbus.SMBus(self.bus)

# we use a lock so that only one peripheral can use the I2C bus
from contextlib import contextmanager
from threading import Lock

_SMBUS_LOCK = Lock()
_SMBUS_LOCK_TIMEOUT_SEC = 0.5

@contextmanager
def _grab_smbus_lock():
  locked = False
  give_up_time = time.time() + _SMBUS_LOCK_TIMEOUT_SEC

  try:
    while True:
      locked = _SMBUS_LOCK.aquire(False)
      if locked:
        yield True
        break

      if time.time() > give_up_time:
        raise SMBUSTimeout(
            "Gave up waiting for the SMBUS after %f seconds" % _SMBUS_LOCK_TIMEOUT_SEC)

  finally:
    if locked:
      _SMBUS_LOCK.release()

_SMBUS.lock_grabber = _grab_smbus_lock

# some constants for I2C
I2C_ALL_CALL = 0x0 # all call address -- goes to all devices (that support it)
I2C_SOFT_RESET = 0x06 # all devices reset

# lets start initializing our peripherals
import Microcontroller
MAPLE = Microcontroller()

import ADS1115
ANALOG1 = ADS1115()

import MCP23017
MCP48 = MCP23017()

ALL_PERIPHERALS = [
    MAPLE,
    ANALOG1,
    MCP48,
    ]

def reset_all():
  # re-initalize any mcp port expanders
  mcps = [p for p in ALL_PERIPHERALS if type(p) == MCP23017]
  if len(mcps) > 0:
    # send a reset to re-init all the mcps
    wiringpi.pinMode(RESET_PIN, wiringpi.OUTPUT)

    wiringpi.digitalWrite(RESET_PIN, 0)
    time.sleep(0.1)
    wiringpi.digitalWrite(RESET_PIN, 1)

    # send initial config to every mcp
    for mcp in mcps:
      mcp.send_init_config()

  # reset any ADC devices
  adcs = [p for p in ALL_PERIPHERALS if type(p) == ADS1115]
  if len(adcs) > 0:
    # i2c all-call reset
    with _SMBUS.lock_grabber():
      self.i2c.write_byte(I2C_ALL_CALL, I2C_SOFT_RESET)

    # send config to any devices
    for adc in adcs:
      adc.write_config()

  # reset any microcontrollers
  micros = [p for p in ALL_PERIPHERALS if type(p) == Microcontroller]
  for micro in micros:
    micro.reset()
