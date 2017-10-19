#!/usr/bin/env python2.7
"""
Contains and manages the current state of the game
"""

from peripherals import *
from controls import *

INPUTS = {
    "red_toggle_1": Switch(
      device = MCP20,
      pin = 1,
      ),
    "red_toggle_2": Input(
      device = MCP20,
      pin = 2,
      ),
    "blue_toggle_1": SwitchWithTwoLights(
      device = MCP20,
      pin = 3,
      up_led_id = 6,
      down_led_id = 7,
      ),
    "Keypad": Keypad({
      1: KeypadButton(MCP20, pin = 4, led_id = 8),
      2: KeypadButton(MCP20, pin = 5, led_id = 9),
      3: KeypadButton(MCP20, pin = 6, led_id = 10),
      4: KeypadButton(MCP20, pin = 7, led_id = 11),
      5: KeypadButton(MCP20, pin = 8, led_id = 12),
      6: KeypadButton(MCP20, pin = 9, led_id = 13),
      7: KeypadButton(MCP20, pin = 10, led_id = 14),
      8: KeypadButton(MCP20, pin = 11, led_id = 15),
      9: KeypadButton(MCP20, pin = 12, led_id = 16),
      0: KeypadButton(MCP20, pin = 14, led_id = 17),
      'input': KeypadButton(MCP20, pin = 13, led_id = 18),
      'ok': KeypadButton(MCP20, pin = 15, led_id = 19),
      }),
    "Accelerator": Accelerator(
      device = ANALOG1,
      pin = 0,
      first_led_id = 10,
      led_count = 20,
      )
    }

def generate(inputs = INPUTS):
  state = {}
  for tag, control in inputs.items():
    control.read()
    state[tag] = control.value

  return state
