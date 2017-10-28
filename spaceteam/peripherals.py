#!/usr/bin/env python2.7
"""
Initializes and provides access to board peripherals
"""

import time
import threading

# initialize GPIO
import wiringpi
wiringpi.wiringPiSetup()

RESET_PIN = 27

# initialize I2C
from spacebus import Spacebus
_SMBUS = Spacebus()

from microcontroller import Microcontroller
MAPLE = Microcontroller("/dev/serial0")

from ads1115 import ADS1115
ANALOG1 = ADS1115(_SMBUS, 0x48)

from mcp23017 import MCP23017
MCP26 = MCP23017(_SMBUS, 0x26)
MCP27 = MCP23017(_SMBUS, 0x27)

ALL = [
    MAPLE,
    MCP26,
    MCP27,
    #ANALOG1,
    ]

def reset_all():
  """resets all peripherals"""
  # reset any microcontrollers
  micros = [p for p in ALL if type(p) == Microcontroller]
  for micro in micros:
    micro.reset()
    time.sleep(3)
    print micro.get_state()

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
      adc.reset()

