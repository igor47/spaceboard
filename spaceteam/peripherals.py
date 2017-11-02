#!/usr/bin/env python2.7
"""
Initializes and provides access to board peripherals
"""

import smbus
import time

# initialize GPIO
import wiringpi
wiringpi.wiringPiSetup()

RESET_PIN = 27

# handling i2c resets
I2C_ALL_CALL = 0x0 # all call address -- goes to all devices (that support it)
I2C_SOFT_RESET = 0x06 # all devices reset
def all_call_reset(bus):
  bus.write_byte(I2C_ALL_CALL, I2C_SOFT_RESET)

# initialize I2C
BUS_ID = 1
_SMBUS = smbus.SMBus(BUS_ID)

from ads1115 import ADS1115
ANALOG1 = ADS1115(_SMBUS, 0x48)

from mcp23017 import MCP23017
MCP24 = MCP23017(_SMBUS, 0x24)
MCP25 = MCP23017(_SMBUS, 0x25)
MCP26 = MCP23017(_SMBUS, 0x26)
MCP27 = MCP23017(_SMBUS, 0x27)

INPUTS = [
    MCP24,
    MCP25,
    MCP26,
    MCP27,
    ANALOG1,
    ]

from microcontroller import Microcontroller
MAPLE = Microcontroller("/dev/serial0")

from ssd1306 import SSD1306
DISPLAY = SSD1306(_SMBUS)

from progress import Progress
PROGRESS = Progress(MAPLE)

OUTPUTS = [
    PROGRESS,
    MAPLE,
    DISPLAY,
    ]

from sound_player import SoundPlayer
SOUNDS = SoundPlayer()

ALL = INPUTS + OUTPUTS
def read_all():
  for p in ALL:
    p.communicate()

def reset_all():
  """resets all peripherals"""
  # start by toggling the reset pin
  wiringpi.pinMode(RESET_PIN, wiringpi.OUTPUT)
  wiringpi.digitalWrite(RESET_PIN, 0)
  time.sleep(0.1)
  wiringpi.digitalWrite(RESET_PIN, 1)

  # initialize the display
  DISPLAY.reset()

  # reset the MAPLE
  MAPLE.reset()
  tries = 0
  while tries < 3:
    time.sleep(0.1)
    try:
      MAPLE.get_state()
    except:
      tries += 1
    else:
      break

  # re-initalize any mcp port expanders
  mcps = [p for p in INPUTS if type(p) == MCP23017]
  for mcp in mcps:
    mcp.reset()

  # reset any ADC devices
  adcs = [p for p in INPUTS if type(p) == ADS1115]
  if len(adcs) > 0:
    all_call_reset(_SMBUS)

    # send config to any devices
    for adc in adcs:
      adc.reset()

  DISPLAY.message = 'READY!'
  SOUNDS.play('bootup')
