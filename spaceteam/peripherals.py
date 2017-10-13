#!/usr/bin/env python2.7
"""
Initializes and provides access to board peripherals
"""

import time
import threading

from errors import *

# initialize GPIO
import wiringpi
wiringpi.wiringPiSetup()

RESET_PIN = 29

# initialize I2C
from spacebus import Spacebus
_SMBUS = Spacebus()

# lets start initializing our peripherals
LED_STRIP = []

import Microcontroller
MAPLE = Microcontroller()

import ADS1115
ANALOG1 = ADS1115()

import MCP23017
MCP48 = MCP23017()

ALL = [
    MAPLE,
    ANALOG1,
    MCP48,
    ]

def reset_all():
  """resets all peripherals

  you'll need to restart the reader thread after calling this"""
  # can't reset and read at the same time!
  stop_reading()

  # re-initalize any mcp port expanders
  mcps = [p for p in ALL if type(p) == MCP23017]
  if len(mcps) > 0:
    # send a reset to re-init all the mcps
    wiringpi.pinMode(RESET_PIN, wiringpi.OUTPUT)

    wiringpi.digitalWrite(RESET_PIN, 0)
    time.sleep(0.1)
    wiringpi.digitalWrite(RESET_PIN, 1)

    # send initial config to every mcp
    for mcp in mcps:
      mcp.reset()

  # reset any ADC devices
  adcs = [p for p in ALL if type(p) == ADS1115]
  if len(adcs) > 0:
    _SMBUS.all_call_reset()

    # send config to any devices
    for adc in adcs:
      adc.write_config()

  # reset any microcontrollers
  micros = [p for p in ALL if type(p) == Microcontroller]
  for micro in micros:
    micro.reset()

