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
      'True': 'Deploy chute!',
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
    'id': "red_arcade_top",
    'control': Switch(
      device = MCP20,
      pin = 0,
    ),
    'actions': {
      'True': 'Launch the nukes.',
    },
  },
  {
    'id': "red_arcade_missles",
    'control': Switch(
      device = MCP20,
      pin = 5,
    ),
    'actions': {
      'True': 'Fire ze missiles!',
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
