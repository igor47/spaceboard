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
      sounds = {False: 'thruster'},
    ),
    'actions': {
      'True': 'Deactivate thrusters',
      'False': 'Activate thrusters!',
    },
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
      'True': 'Vent the airlock!',
      'False': 'Pressurize airlock.',
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
      'True': 'Transducer to blue',
      'False': 'Transducer to orange',
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
      'True': 'Freeze the cryo-fan',
      'False': 'Spin the cryo-fan',
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
      'True': 'Ungimbal the gimbal',
      'False': 'Gimbal the gimbal',
    }
  },
  {
    'id': "silver_toggle_bottom_2",
    'control': SwitchWithTwoLights(
      device = MCP27,
      pin = 8,
      led_up_id = 12,
      led_down_id = 15,
      sounds = {False: 'spacedoor'},
    ),
    'actions': {
      'True': 'Close pod bay doors',
      'False': 'Open pod bay doors',
    }
  },
  {
    'id': "silver_toggle_bottom_3",
    'control': SwitchWithTwoLights(
      device = MCP26,
      pin = 8,
      led_up_id = 11,
      led_down_id = 16,
      sounds = {False: 'ping'},
    ),
    'actions': {
      'True': 'Unping.',
      'False': 'Ping!',
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
      'True': 'End system test',
      'False': 'Test the system!',
    }
  },
  {
    'id': "little_red_push",
    'control': Switch(
      device = MCP27,
      pin = 9,
    ),
    'actions': {
      'True': 'Ingest waste',
    },
  },
  {
    'id': "little_green_push",
    'control': Switch(
      device = MCP27,
      pin = 10,
    ),
    'actions': {
      'True': 'Flush waste!'
    },
  },
  {
    'id': "big_green_push",
    'control': Switch(
      device = MCP25,
      pin = 0,
      sounds = {False: 'warp'}
    ),
    'actions': {
      'False': 'Engage hyperdrive!'
    },
  },
  {
    'id': "big_red_push",
    'control': Switch(
      device = MCP25,
      pin = 15,
      sounds = {False: 'unwarp'}
    ),
    'actions': {
      'False': 'Disengage hyperdrive!'
    },
  },
  {
    'id': "red_rocket_5",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 6,
      sounds = {True: 'robot', False: 'robot-complain'},
    ),
    'actions': {
      'True': 'Hire autopilot',
      'False': 'Fire autopilot',
    }
  },
  {
    'id': "red_rocket_4",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 7,
    ),
    'actions': {
      'True': 'Pull a Crazy Ivan',
      'False': 'Pacify Crazy Ivan',
    }
  },
  {
    'id': "red_rocket_3",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 1,
      sounds = {True: 'shield-up', False: 'shield-down'},
    ),
    'actions': {
      'True': 'Raise shields!',
      'False': 'Lower shields!',
    }
  },
  {
    'id': "red_rocket_2",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 2,
      sounds = {True: 'siren'},
    ),
    'actions': {
      'True': 'Eject the pilot!',
      'False': 'Reseat the pilot!',
    }
  },
  {
    'id': "red_rocket_1",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 5,
      sounds = {False: 'explosion'},
    ),
    'actions': {
      'True': 'Launch missiles!',
      'False': 'Abort missile launch!',
    }
  },
  {
    'id': "yellow_rocket_3",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 0,
    ),
    'actions': {
      'True': 'Modulate the shields',
      'False': 'Demodulate the shields!',
    }
  },
  {
    'id': "yellow_rocket_2",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 3,
    ),
    'actions': {
      'True': 'Eject cargo!',
      'False': 'Uneject cargo!'
    }
  },
  {
    'id': "yellow_rocket_1",
    'control': SwitchWithPulldown(
      device = MCP24,
      pin = 6,
    ),
    'actions': {
      'True': 'Arm the missiles',
      'False': 'Disarm the missiles'
    }
  },
  {
    'id': "red_rocker_1",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 2,
    ),
    'actions': {
      'True': 'Activate plasma containment',
      'False': 'Uncontain the plasma'
    }
  },
  {
    'id': "red_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 1,
    ),
    'actions': {
      'True': 'Phase-shift the plasma',
      'False': 'Phase-lock the plasma'
    }
  },
  {
    'id': "red_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 4,
    ),
    'actions': {
      'True': 'Intercool the plasma',
      'False': 'Disable plasma intercool',
    }
  },
  {
    'id': "red_rocker_4",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 3,
    ),
    'actions': {
      'True': 'Discharge plasma',
      'False': 'Un-Discharge plasma',
    }
  },
  {
    'id': "green_rocker_1",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 8,
    ),
    'actions': {
      'True': 'Power to level 10',
      'False': 'Shut off power to level 10',
    }
  },
  {
    'id': "green_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 10,
    ),
    'actions': {
      'True': 'Power to broom closet!',
      'False': 'Turn off power to broom closet!',
    }
  },
  {
    'id': "green_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 9,
    ),
    'actions': {
      'True': 'Activate auxillary power!',
      'False': 'Switch to mains power!',
    }
  },
  {
    'id': "green_rocker_4",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 12,
    ),
    'actions': {
      'True': 'Power to enemy ships',
      'False': 'Stop powering enemy ships!',
    }
  },
  {
    'id': "blue_rocker_1",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 5,
    ),
    'actions': {
      'True': 'Chill the coolant',
      'False': 'Warm the coolant',
    }
  },
  {
    'id': "blue_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 14,
    ),
    'actions': {
      'True': 'Vent coolant!',
      'False': 'Inspire coolant!',
    }
  },
  {
    'id': "blue_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 11,
    ),
    'actions': {
      'True': 'Stir coolant',
      'False': 'Congeal coolant',
    }
  },
  {
    'id': "blue_rocker_4",
    'control': SwitchWithPulldown(
      device = MCP25,
      pin = 13,
    ),
    'actions': {
      'True': 'Pump coolant',
      'False': 'Leak coolant',
    }
  },
  {
    'id': "red_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 4,
      sounds = {True: 'ka-ching',},
    ),
    'actions': {
      'True': 'Invoice passengers!'
    },
  },
  {
    'id': "red_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 7,
    ),
    'actions': {
      'True': 'Terminate passengers',
    },
  },
  {
    'id': "white_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 9,
      sounds = {True: 'makeitso'},
    ),
    'actions': {
      'True': 'Make it so!',
    },
  },
  {
    'id': "white_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 8,
    ),
    'actions': {
      'True': 'Abuse power!',
    },
  },
  {
    'id': "yellow_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 15,
    ),
    'actions': {
      'True': 'Sedate passengers',
    },
  },
  {
    'id': "yellow_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 12,
    ),
    'actions': {
      'True': 'Sedate passengers!',
    },
  },
  {
    'id': "blue_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 11,
      sounds = {False: 'laser'}
    ),
    'actions': {
      'True': 'Fire lasers!',
    },
  },
  {
    'id': "blue_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 10,
      sounds = {False: 'horn'}
    ),
    'actions': {
      'True': 'Honk the spacehorn!',
    },
  },
  {
    'id': "green_arcade_2",
    'control': Switch(
      device = MCP24,
      pin = 14,
    ),
    'actions': {
      'True': 'Feed the passengers',
    },
  },
  {
    'id': "green_arcade_1",
    'control': Switch(
      device = MCP24,
      pin = 13,
    ),
    'actions': {
      'True': 'Brew tea!',
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
    'actions': {"%03d" % n: "Set course to %d!" % n for n in xrange(999)}
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
