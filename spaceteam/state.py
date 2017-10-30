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
    "silver_toggle_top_1": SwitchWithTwoLights(
      device = MCP26,
      pin = 10,
      led_up_id = 5,
      led_down_id = 6,
      ),
    "silver_toggle_top_2": SwitchWithTwoLights(
      device = MCP26,
      pin = 12,
      led_up_id = 4,
      led_down_id = 7,
      ),
    "silver_toggle_top_3": SwitchWithTwoLights(
      device = MCP26,
      pin = 13,
      led_up_id = 3,
      led_down_id = 8,
      ),
    "silver_toggle_top_4": SwitchWithTwoLights(
      device = MCP26,
      pin = 11,
      led_up_id = 2,
      led_down_id = 9,
      ),
    "silver_toggle_bottom_1": SwitchWithTwoLights(
      device = MCP26,
      pin = 9,
      led_up_id = 13,
      led_down_id = 14,
      ),
    "silver_toggle_bottom_2": SwitchWithTwoLights(
      device = MCP27,
      pin = 8,
      led_up_id = 12,
      led_down_id = 15,
      ),
    "silver_toggle_bottom_3": SwitchWithTwoLights(
      device = MCP26,
      pin = 8,
      led_up_id = 11,
      led_down_id = 16,
      ),
    "silver_toggle_bottom_4": SwitchWithTwoLights(
      device = MCP26,
      pin = 14,
      led_up_id = 10,
      led_down_id = 17,
      ),
    "little_red_push": Switch(
      device = MCP27,
      pin = 9,
      ),
    "little_green_push": Switch(
      device = MCP27,
      pin = 10,
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
