#!/usr/bin/env python2.7
"""
Contains and manages the current state of the game
"""

from peripherals import *
from controls import *

INPUTS = [
  {
    'id': 'power',
    'control': SwitchWithLight(
      device = MCP27,
      pin = 11,
      led_id = 1,
      ),
    'actions': {
      'True': 'Push the power button',
    }
  },
  {
    'id': 'silver_toggle_top_1',
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 10,
      led_up_id = 5,
      led_down_id = 6,
    ),
    'type': 'switch',
    'description': 'first silver toggle switch in the top row',
  },
  {
    'id': "silver_toggle_top_2",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 12,
      led_up_id = 4,
      led_down_id = 7,
      ),
    'type': 'switch',
    'description': 'second silver toggle switch in the top row',
  },
  {
    'id': "silver_toggle_top_3",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 13,
      led_up_id = 3,
      led_down_id = 8,
    ),
    'type': 'switch',
    'description': 'third silver toggle switch in the top row',
  },
  {
    'id': "silver_toggle_top_4",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 11,
      led_up_id = 2,
      led_down_id = 9,
    ),
    'type': 'switch',
    'description': 'last silver toggle switch in the top row',
  },
  {
    'id': "silver_toggle_bottom_1",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 9,
      led_up_id = 13,
      led_down_id = 14,
    ),
    'type': 'switch',
    'description': 'first silver toggle switch in the bottom row',
  },
  {
    'id': "silver_toggle_bottom_2",
    'control': SwitchWithTwoLights(
      device = MCP27,
      pin = 8,
      led_up_id = 12,
      led_down_id = 15,
    ),
    'type': 'switch',
    'description': 'second silver toggle switch in the bottom row',
  },
  {
    'id': "silver_toggle_bottom_3",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 8,
      led_up_id = 11,
      led_down_id = 16,
    ),
    'type': 'switch',
    'description': 'third silver toggle switch in the bottom row',
  },
  {
    'id': "silver_toggle_bottom_4",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 14,
      led_up_id = 10,
      led_down_id = 17,
    ),
    'type': 'switch',
    'description': 'last silver toggle switch in the bottom row',
  },
  {
    'id': "little_red_push",
    'control': Switch(
      device = MCP27,
      pin = 9,
    ),
    'actions': {
      'True': 'Push the little red pushbutton!',
    },
  },
  {
    'id': "little_green_push",
    'control': Switch(
      device = MCP27,
      pin = 10,
    ),
    'actions': {
      'True': 'Push the little green pushbutton!'
    },
  },
  {
    'id': 'keypad',
    'control': Keypad({
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
    'actions': {"%03d" % n: "Set the keypad to %d!" % n for n in xrange(999)}
  },
  {
    'id': 'Accelerator',
    'control': Accelerator(
       device = ANALOG1,
       pin = 0,
       first_led_id = 30,
       led_count = 15,
     ),
    'actions': {str(n): "Set the accelerator to %d!" % n for n in xrange(50)}
  }
]

for i in INPUTS:
  if 'type' in i and i['type'] == 'switch':
    i['actions'] = {
      'True': "Set the %s to ON" % i['description'],
      'False': "Set the %s to OFF" % i['description'],
    }

def announce(inputs = INPUTS):
  controls = []
  for i in inputs:
    i['control'].read()
    c = {
      'id': i['id'],
      'state': str(i['control'].value),
      'actions': i['actions']
      }
    controls.append(c)

  return {'controls': controls}

def generate(inputs = INPUTS):
  state = {}
  for i in inputs:
    i['control'].read()
    state[i['id']] = i['control'].value

  return state
