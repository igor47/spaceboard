#!/usr/bin/env python2.7
"""
Contains and manages the current state of the game
"""

from peripherals import *
from controls import *
from seven_segment import SevenSegment

INPUTS = [
  {
    'id': "top_left_rocket_yellow",
    'control': Switch(
      device = MCP20,
      pin = 4,
    ),
    'actions': {
      'True': 'Hire autopilot',
      'False': 'Fire autopilot',
    },
  },
  {
    'id': "top_left_rocket_yellow",
    'control': Switch(
      device = MCP20,
      pin = 4,
    ),
    'actions': {
      'True': 'Turn on yellow rocket',
      'False': 'Turn off yellow rocket',
    },
  },

  {
    'id': "blue_arcade_landing",
    'control': Switch(
      device = MCP20,
      pin = 8,
    ),
    'actions': {
      'False': 'Deploy chute!',
    },
  },
  {
    'id': "landing_rocker_1",
    'control': SwitchWithPulldown(
      device = MCP20,
      pin = 9,
    ),
    'actions': {
      'True': 'Lower landing gear.',
      'False': 'Raise landing gear.',
    }
  },
  {
    'id': "landing_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP20,
      pin = 13,
    ),
    'actions': {
      'True': 'Flap the flaps!',
      'False': 'Unflap the flaps.',
    }
  },
  {
    'id': "landing_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP20,
      pin = 10,
    ),
    'actions': {
      'True': 'Unfurl the ramp.',
      'False': 'Bring in the ramp.',
    }
  },
  {
    'id': "landing_rocker_4",
    'control': SwitchWithPulldown(
      device = MCP20,
      pin = 12,
    ),
    'actions': {
      'True': 'Emergency flashers!',
      'False': 'End the emergency.',
    }
  },
  {
    'id': "landing_rocker_5",
    'control': SwitchWithPulldown(
      device = MCP20,
      pin = 12,
    ),
    'actions': {
      'True': 'Set the parking brake.',
      'False': 'Release parking brake.',
    }
  },
  {
    'id': "airlock_rocker_1",
    'control': SwitchWithPulldown(
      device = MCP20,
      pin = 3,
    ),
    'actions': {
      'True': 'Open external airlock door',
      'False': 'Close external airlock door!',
    }
  },
  {
    'id': "airlock_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP20,
      pin = 2,
    ),
    'actions': {
      'True': 'Open inner airlock door.',
      'False': 'Close inner airlock door!',
    }
  },
  {
    'id': "airlock_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP20,
      pin = 1,
    ),
    'actions': {
      'True': 'Pressurize the airock!',
      'False': 'Vent the airlock.',
    }
  },
  {
    'id': "nuke_arcade",
    'control': Switch(
      device = MCP20,
      pin = 0,
    ),
    'actions': {
      'True': 'Launch the nukes.',
    },
  },
  {
    'id': "nuke_key",
    'control': Switch(
      device = MCP20,
      pin = 7,
    ),
    'actions': {
      'True': 'Hasten nuclear apocalypse',
      'False': 'Stand down from nuclear apocalypse',
    },
  },

  {
    'id': "weapons_red_arcade",
    'control': Switch(
      device = MCP20,
      pin = 5,
    ),
    'actions': {
      'False': 'Fire ze missiles!',
    },
  },
  {
    'id': "weapons_yellow_arcade",
    'control': Switch(
      device = MCP21,
      pin = 14,
    ),
    'actions': {
      'False': 'Fire lasers!',
    },
  },
  {
    'id': "weapons_white_aracde",
    'control': Switch(
      device = MCP21,
      pin = 0,
    ),
    'actions': {
      'False': 'Chaff!',
    },
  },

  {
    'id': "manuevers_yellow_arcade",
    'control': Switch(
      device = MCP21,
      pin = 4,
    ),
    'actions': {
      'False': 'Pu1l a CraZy IvaN.',
    },
  },
  {
    'id': "manuevers_green_arcade",
    'control': Switch(
      device = MCP21,
      pin = 1,
    ),
    'actions': {
      'False': 'Evasive manuevers!',
    },
  },
  {
    'id': "manuevers_blue_arcade",
    'control': Switch(
      device = MCP21,
      pin = 2,
    ),
    'actions': {
      'False': 'Do a barrel roll!',
    },
  },

  {
    'id': "misc_white_arcade",
    'control': Switch(
      device = MCP21,
      pin = 5,
    ),
    'actions': {
      'False': 'Dump waste!',
    },
  },
  {
    'id': "misc_green_arcade",
    'control': Switch(
      device = MCP21,
      pin = 1,
    ),
    'actions': {
      'False': 'Green button next to "dump waste"',
    },
  },

  {
    'id': "silver_toggle_top_1",
    'control': SwitchWithLed(
      device = MCP27,
      pin = 15,
      array_idx = 59,
    ),
    'actions': {
      'True': 'Freeze the cryofan',
      'False': 'Spin the cryofan',
    },
  },
  {
    'id': "silver_toggle_top_2",
    'control': SwitchWithLed(
      device = MCP27,
      pin = 15,
      array_idx = 33,
    ),
    'actions': {
      'False': 'Transduce the transducer!',
      'True': 'Untransduce!',
    },
  },
  {
    'id': "silver_toggle_top_3",
    'control': SwitchWithLed(
      device = MCP27,
      pin = 13,
      array_idx = 56,
    ),
    'actions': {
      'True': 'Close pod bay doors',
      'False': 'Open pod bay doors',
    },
  },
  {
    'id': "silver_toggle_top_4",
    'control': SwitchWithLed(
      device = MCP27,
      pin = 11,
      array_idx = 57,
    ),
    'actions': {
      'True': "You've had enough coffee.",
      'False': 'Brew coffee',
    },
  },

  {
    'id': "silver_toggle_bottom_1",
    'control': SwitchWithLed(
      device = MCP27,
      pin = 12,
      array_idx = 44,
    ),
    'actions': {
      'True': 'Ungimbal the gimbal',
      'False': 'Gimbal!',
    },
  },
  {
    'id': "silver_toggle_bottom_2",
    'control': SwitchWithLed(
      device = MCP27,
      pin = 14,
      array_idx = 19,
    ),
    'actions': {
      'True': 'Stop thrusting.',
      'False': 'Thrust your thrusters.',
    },
  },
  {
    'id': "silver_toggle_bottom_3",
    'control': SwitchWithLed(
      device = MCP27,
      pin = 9,
      array_idx = 60,
    ),
    'actions': {
      'True': 'De-Ping!',
      'False': 'Ping!',
    },
  },
  {
    'id': "silver_toggle_bottom_4",
    'control': SwitchWithLed(
      device = MCP27,
      pin = 8,
      array_idx = 18,
    ),
    'actions': {
      'True': "Don't TEST me',
      'False': 'Test the system!',
    },
  },

  {
    'id': "big_button_green",
    'control': Switch(
      device = MCP26,
      pin = 10,
    ),
    'actions': {
      'False': 'Make it so!',
    },
  },
  {
    'id': "big_button_red",
    'control': Switch(
      device = MCP26,
      pin = 12,
    ),
    'actions': {
      'False': 'Honk the spacehorn!',
    },
  },

  {
    'id': "power_toggle_green",
    'control': Switch(
      device = MCP26,
      pin = 8,
      array_idx = 46,
    ),
    'actions': {
      'True': 'Main power on!',
      'False': 'Main power off!',
    },
  },
  {
    'id': "power_toggle_red",
    'control': SwitchWithLed(
      device = MCP26,
      pin = 8,
      array_idx = 20,
    ),
    'actions': {
      'True': 'Route auxillary power!',
      'False': 'Deactivate auxillary power',
    },
  },
  {
    'id': "power_toggle_blue",
    'control': Switch(
      device = MCP26,
      pin = 15,
      array_idx = 17,
    ),
    'actions': {
      'True': 'ABSOLUTE POWER',
      'False': 'Relative power.',
    },
  },
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

  return controls

def generate(inputs = INPUTS):
  state = {}
  for i in inputs:
    i['control'].read()
    state[i['id']] = i['control'].value

  return state
