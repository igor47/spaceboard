#!/usr/bin/env python2.7
"""
Contains and manages the current state of the game
"""

from peripherals import *
from controls import *
from seven_segment import SevenSegment

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
    'actions': {
      'True': 'Set the first silver toggle switch in the top row to blue',
      'False': 'Set the first silver toggle switch in the top row to orange',
    }
  },
  {
    'id': "silver_toggle_top_2",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 12,
      led_up_id = 4,
      led_down_id = 7,
      ),
    'actions': {
      'True': 'Set the second silver toggle switch in the top row to blue',
      'False': 'Set the second silver toggle switch in the top row to orange',
    }
  },
  {
    'id': "silver_toggle_top_3",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 13,
      led_up_id = 3,
      led_down_id = 8,
    ),
    'actions': {
      'True': 'Set the third silver toggle switch in the top row to blue',
      'False': 'Set the third silver toggle switch in the top row to orange',
    }
  },
  {
    'id': "silver_toggle_top_4",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 11,
      led_up_id = 2,
      led_down_id = 9,
    ),
    'actions': {
      'True': 'Set the last silver toggle switch in the top row to blue',
      'False': 'Set the last silver toggle switch in the top row to orange',
    }
  },
  {
    'id': "silver_toggle_bottom_1",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 9,
      led_up_id = 13,
      led_down_id = 14,
    ),
    'actions': {
      'True': 'Set the first silver toggle switch in the bottom row to blue',
      'False': 'Set the first silver toggle switch in the bottom row to orange',
    }
  },
  {
    'id': "silver_toggle_bottom_2",
    'control': SwitchWithTwoLights(
      device = MCP27,
      pin = 8,
      led_up_id = 12,
      led_down_id = 15,
    ),
    'actions': {
      'True': 'Set the second silver toggle switch in the bottom row to blue',
      'False': 'Set the second silver toggle switch in the bottom row to orange',
    }
  },
  {
    'id': "silver_toggle_bottom_3",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 8,
      led_up_id = 11,
      led_down_id = 16,
    ),
    'actions': {
      'True': 'Set the third silver toggle switch in the bottom row to blue',
      'False': 'Set the third silver toggle switch in the bottom row to orange',
    }
  },
  {
    'id': "silver_toggle_bottom_4",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 14,
      led_up_id = 10,
      led_down_id = 17,
    ),
    'actions': {
      'True': 'Set the last silver toggle switch in the bottom row to blue',
      'False': 'Set the last silver toggle switch in the bottom row to orange',
    }
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
    'id': "big_green_push",
    'control': Switch(
      device = MCP25,
      pin = 0,
    ),
    'actions': {
      'True': 'Push the big green pushbutton!'
    },
  },
  {
    'id': "big_red_push",
    'control': Switch(
      device = MCP25,
      pin = 15,
    ),
    'actions': {
      'True': 'Push the big red pushbutton!'
    },
  },
  {
    'id': "red_rocket_5",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 6,
    ),
    'type': 'switch',
    'description': 'fifth red rocket toggle',
  },
  {
    'id': "red_rocket_4",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 7,
    ),
    'type': 'switch',
    'description': 'fourth red rocket toggle',
  },
  {
    'id': "red_rocket_3",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 1,
    ),
    'type': 'switch',
    'description': 'third red rocket toggle',
  },
  {
    'id': "red_rocket_2",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 2,
    ),
    'type': 'switch',
    'description': 'second red rocket toggle',
  },
  {
    'id': "red_rocket_1",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 5,
    ),
    'type': 'switch',
    'description': 'first red rocket toggle',
  },
  {
    'id': "yellow_rocket_3",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 0,
    ),
    'type': 'switch',
    'description': 'last yellow rocket toggle',
  },
  {
    'id': "yellow_rocket_2",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 3,
    ),
    'type': 'switch',
    'description': 'second yellow rocket toggle',
  },
  {
    'id': "yellow_rocket_1",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 6,
    ),
    'type': 'switch',
    'description': 'first yellow rocket toggle',
  },
  {
    'id': "red_rocker_1",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 2,
    ),
    'type': 'switch',
    'description': 'first red rocker',
  },
  {
    'id': "red_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 1,
    ),
    'type': 'switch',
    'description': 'second red rocker',
  },
  {
    'id': "red_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 4,
    ),
    'type': 'switch',
    'description': 'third red rocker',
  },
  {
    'id': "red_rocker_4",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 3,
    ),
    'type': 'switch',
    'description': 'last red rocker',
  },
  {
    'id': "green_rocker_1",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 8,
    ),
    'type': 'switch',
    'description': 'first green rocker',
  },
  {
    'id': "green_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 10,
    ),
    'type': 'switch',
    'description': 'second green rocker',
  },
  {
    'id': "green_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 9,
    ),
    'type': 'switch',
    'description': 'third green rocker',
  },
  {
    'id': "green_rocker_4",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 12,
    ),
    'type': 'switch',
    'description': 'last green rocker',
  },
  {
    'id': "blue_rocker_1",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 5,
    ),
    'type': 'switch',
    'description': 'first blue rocker',
  },
  {
    'id': "blue_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 14,
    ),
    'type': 'switch',
    'description': 'second blue rocker',
  },
  {
    'id': "blue_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 11,
    ),
    'type': 'switch',
    'description': 'third blue rocker',
  },
  {
    'id': "blue_rocker_4",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 13,
    ),
    'type': 'switch',
    'description': 'last blue rocker',
  },
  {
    'id': "red_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 4,
    ),
    'actions': {
      'True': 'Push the second red arcade button!'
    },
  },
  {
    'id': "red_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 7,
    ),
    'actions': {
      'True': 'Push the first red arcade button!'
    },
  },
  {
    'id': "white_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 9,
    ),
    'actions': {
      'True': 'Push the second white arcade button!'
    },
  },
  {
    'id': "white_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 8,
    ),
    'actions': {
      'True': 'Push the first white arcade button!'
    },
  },
  {
    'id': "yellow_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 15,
    ),
    'actions': {
      'True': 'Push the second yellow arcade button!'
    },
  },
  {
    'id': "yellow_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 12,
    ),
    'actions': {
      'True': 'Push the first yellow arcade button!'
    },
  },
  {
    'id': "blue_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 11,
    ),
    'actions': {
      'True': 'Push the second blue arcade button!'
    },
  },
  {
    'id': "blue_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 10,
    ),
    'actions': {
      'True': 'Push the first blue arcade button!'
    },
  },
  {
    'id': "green_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 14,
    ),
    'actions': {
      'True': 'Push the second green arcade button!'
    },
  },
  {
    'id': "green_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 13,
    ),
    'actions': {
      'True': 'Push the first green arcade button!'
    },
  },
  {
    'id': 'keypad',
    'control': Keypad(
      buttons = {
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
      },
      displays = [
        SevenSegment({
          'dot': (MCP22, 6),
          'top': (MCP23, 6),
          'left_top': (MCP22, 7),
          'left_bottom': (MCP22, 5),
          'right_top': (MCP23, 4),
          'right_bottom': (MCP22, 9),
          'middle': (MCP22, 13),
          'bottom': (MCP22, 3),
          }),
        SevenSegment({
          'dot': (MCP22, 8),
          'top': (MCP23, 2),
          'left_top': (MCP22, 11),
          'left_bottom': (MCP23, 11),
          'right_top': (MCP23, 3),
          'right_bottom': (MCP23, 12),
          'middle': (MCP23, 8),
          'bottom': (MCP23, 13),
          }),
        SevenSegment({
          'dot': (MCP22, 2),
          'top': (MCP23, 7),
          'left_top': (MCP22, 10),
          'left_bottom': (MCP23, 10),
          'right_top': (MCP23, 9),
          'right_bottom': (MCP22, 12),
          'middle': (MCP23, 5),
          'bottom': (MCP22, 4),
          }),
      ],
    ),
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
    'actions': {str(n): "Set throttle to %d!" % n for n in xrange(15)}
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
