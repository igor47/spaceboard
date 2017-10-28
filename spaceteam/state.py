#!/usr/bin/env python2.7
"""
Contains and manages the current state of the game
"""

from peripherals import *
from controls import *

INPUTS = {
    "power": SwitchWithLight(
      device = MCP27,
      pin = 11,
      led_id = 1,
      ),
    "red_toggle_1": Switch(
      device = MCP26,
      pin = 1,
      ),
    "red_toggle_2": Switch(
      device = MCP26,
      pin = 2,
      ),
    "blue_toggle_1": SwitchWithTwoLights(
      device = MCP26,
      pin = 3,
      led_up_id = 6,
      led_down_id = 7,
      ),
    "Keypad": Keypad({
      1: KeypadButton(MCP27, pin = 15, led_id = 18),
      2: KeypadButton(MCP27, pin = 14, led_id = 25),
      3: KeypadButton(MCP27, pin = 13, led_id = 26),
      4: KeypadButton(MCP27, pin = 12, led_id = 19),
      5: KeypadButton(MCP27, pin = 0, led_id = 24),
      6: KeypadButton(MCP27, pin = 1, led_id = 27),
      7: KeypadButton(MCP27, pin = 2, led_id = 20),
      8: KeypadButton(MCP27, pin = 3, led_id = 23),
      9: KeypadButton(MCP27, pin = 4, led_id = 28),
      0: KeypadButton(MCP27, pin = 6, led_id = 22),
      'input': KeypadButton(MCP27, pin = 5, led_id = 21),
      'ok': KeypadButton(MCP27, pin = 7, led_id = 29),
      }),
     "Accelerator": Accelerator(
       device = ANALOG1,
       pin = 0,
       first_led_id = 30,
       led_count = 15,
       )
     }

def generate(inputs = INPUTS):
  state = {}
  for tag, control in inputs.items():
    control.read()
    state[tag] = control.value

  return state
