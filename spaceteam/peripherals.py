#!/usr/bin/env python2.7
"""
Initializes and provides access to board peripherals
"""

import time

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
MCP24 = MCP23017(_SMBUS, 0x24)
MCP25 = MCP23017(_SMBUS, 0x25)
MCP26 = MCP23017(_SMBUS, 0x26)
MCP27 = MCP23017(_SMBUS, 0x27)

from ssd1306 import SSD1306
DISPLAY = SSD1306(_SMBUS)

from progress import Progress
PROGRESS = Progress(MAPLE)

from sound_player import SoundPlayer
SOUNDS = SoundPlayer()

ALL = [
    DISPLAY,
    MAPLE,
    MCP24,
    MCP25,
    MCP26,
    MCP27,
    ANALOG1,
    PROGRESS,
    SOUNDS,
    ]

def reset_all():
  """resets all peripherals"""
  # start by toggling the reset pin
  wiringpi.pinMode(RESET_PIN, wiringpi.OUTPUT)
  wiringpi.digitalWrite(RESET_PIN, 0)
  time.sleep(0.1)
  wiringpi.digitalWrite(RESET_PIN, 1)

  # initialize the display
  DISPLAY.reset()

  # reset any microcontrollers
  micros = [p for p in ALL if type(p) == Microcontroller]
  for micro in micros:
    micro.reset()
    tries = 0
    while tries < 3:
      time.sleep(0.1)
      try:
        micro.get_state()
      except:
        tries += 1
      else:
        break

  # re-initalize any mcp port expanders
  mcps = [p for p in ALL if type(p) == MCP23017]
  if len(mcps) > 0:
    for mcp in mcps:
      mcp.reset()

  # reset any ADC devices
  adcs = [p for p in ALL if type(p) == ADS1115]
  if len(adcs) > 0:
    _SMBUS.all_call_reset()

    # send config to any devices
    for adc in adcs:
      adc.reset()

  DISPLAY.message = 'READY!'
  SOUNDS.play('bootup')
