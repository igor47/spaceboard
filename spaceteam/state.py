#!/usr/bin/env python2.7
"""
Contains and manages the current state of the game
"""

from peripherals import *
from controls import *
from seven_segment import SevenSegment

INPUTS = [
  {
    'id': "top_left_rocket_red",
    'control': Switch(
      device = MCP20,
      pin = 4,
    ),
    'actions': {
      'True': 'Red alert! Battle stations!',
      'False': 'Stand down from red alert',
    },
  },
  {
    'id': "top_left_rocket_yellow",
    'control': Switch(
      device = MCP20,
      pin = 6,
      sounds = {True: 'robot', False: 'robot-complain'},
    ),
    'actions': {
      'True': 'Hire autopilot!',
      'False': 'Fire the autopilot (for drinking)',
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
      pin = 14,
    ),
    'actions': {
      'True': 'Set the parking brake.',
      'False': 'Release parking brake.',
    }
  },

  {
    'id': 'turn_signal_left',
    'control': SwitchWithLed(
      device = MCP20,
      pin = 15,
      array_idx = 47,
      blink = True,
    ),
    'actions': {
      'False': 'Indicate left turn!',
      'True': 'Turn signal off!',
    },
  },
  {
    'id': 'turn_signal_right',
    'control': SwitchWithLed(
      device = MCP20,
      pin = 11,
      array_idx = 58,
      blink = True,
    ),
    'actions': {
      'False': 'Indicate right turn!',
      'True': 'Turn signal off!',
    },
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
    'id': 'big_knob_pusher',
    'control': Switch(
      device = MCP21,
      pin = 9,
    ),
    'actions': {
      'True': 'Push the BIG KNOB!',
    },
  },
  {
    'id': 'big_knob_spinner',
    'control': RotaryEncoder(
      switch_a = Switch(device = MCP21, pin = 11),
      switch_b = Switch(device = MCP21, pin = 10),
    ),
    'actions': {
      'clockwise': 'Spin the BIG KNOB clockwise!',
      'counter': 'Spin the BIG KNOB backwards!',
    },
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
    'control': SwitchWithLed(
      device = MCP20,
      pin = 7,
      array_idx = 32,
      blink = True,
      backwards = True,
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
      sounds = {False: 'explosion'},
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
      sounds = {False: 'laser'}
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
    'id': 'weapons_red_rocket_top',
    'control': Switch(
      device = MCP21,
      pin = 12,
    ),
    'actions': {
      'True': 'Arm missiles',
      'False': 'Disarm missiles',
    },
  },
  {
    'id': 'weapons_red_rocket_bottom',
    'control': Switch(
      device = MCP21,
      pin = 3,
      sounds = {True: 'shield-up', False: 'shield-down'},
    ),
    'actions': {
      'True': 'Raise shields',
      'False': 'Lower shields',
    },
  },
  {
    'id': 'rotary_with_leds',
    'control': ShieldModulator(
      encoder = RotaryEncoder(
        switch_a = Switch(device = MCP21, pin = 8),
        switch_b = Switch(device = MCP21, pin = 13),
      ),
      first_led = 2,
      led_count = 12
    ),
    'actions': {
      c['name']:'Set shield modulation to %s' % c['name'] for c in ShieldModulator.COLORS
    }
  },
  {
    'id': 'weapons_yellow_rocket',
    'control': Switch(
      device = MCP21,
      pin = 7,
    ),
    'actions': {
      'True': 'Arm lasers',
      'False': 'Disarm lasers',
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
      pin = 6,
    ),
    'actions': {
      'False': 'Bother tech support!',
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
      pin = 10,
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
      sounds = {False: 'spacedoor'},
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
      sounds = {False: 'thruster'},
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
      sounds = {False: 'ping'},
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
      'True': "Don't TEST me",
      'False': 'Test the system!',
    },
  },

  {
    'id': "big_button_green",
    'control': Switch(
      device = MCP26,
      pin = 10,
      sounds = {False: 'makeitso'},
    ),
    'actions': {
      'False': 'Make it so!',
    },
  },
  {
    'id': "big_button_red",
    'control': Switch(
      device = MCP26,
      pin = 9,
      sounds = {False: 'horn'}
    ),
    'actions': {
      'False': 'Honk the spacehorn!',
    },
  },

  {
    'id': "power_toggle_green",
    'control': SwitchWithLed(
      device = MCP26,
      pin = 8,
      array_idx = 46,
      backwards = True,
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
      pin = 15,
      array_idx = 20,
      backwards = True,
    ),
    'actions': {
      'True': 'Route auxillary power!',
      'False': 'Deactivate auxillary power',
    },
  },
  {
    'id': "power_toggle_blue",
    'control': SwitchWithLed(
      device = MCP26,
      pin = 13,
      array_idx = 17,
      backwards = True,
    ),
    'actions': {
      'True': 'ABSOLUTE POWER',
      'False': 'Relative power.',
    },
  },

  {
    'id': 'on_off_toggle_1',
    'control': Switch(
      device = MCP26,
      pin = 12,
    ),
    'actions': {
      'False': 'Re-route power to level 10',
      'True': 'Shut off power to level 10',
    },
  },
  {
    'id': 'on_off_toggle_2',
    'control': Switch(
      device = MCP26,
      pin = 11,
    ),
    'actions': {
      'False': 'Activate massage chair',
      'True': 'Deactivate message chair',
    },
  },
  {
    'id': 'flight_rocker_1',
    'control': SwitchWithPulldown(
      device = MCP26,
      pin = 14,
    ),
    'actions': {
      'True': 'Activate infinite improbability drive',
      'False': 'Restore normal probability',
    }
  },
  {
    'id': "flight_rocker_2",
    'control': SwitchWithPulldown(
      device = MCP26,
      pin = 3,
    ),
    'actions': {
      'True': 'Stir coolant',
      'False': 'Congeal coolant',
    }
  },
  {
    'id': "flight_rocker_3",
    'control': SwitchWithPulldown(
      device = MCP27,
      pin = 0,
    ),
    'actions': {
      'True': 'Activate plasma containment field',
      'False': 'Disperse plasma containment field',
    }
  },
  {
    'id': "flight_rocker_4",
    'control': SwitchWithPulldown(
      device = MCP26,
      pin = 6,
      sounds = {True: 'modem'},
    ),
    'actions': {
      'True': 'Enter cyberspace',
      'False': 'Exit cyberspace',
    }
  },

  {
    'id': 'keypad',
    'control': Keypad(
      buttons = {
        1: KeypadButton(MCP27, pin = 6, led_id = 14),
        2: KeypadButton(MCP27, pin = 4, led_id = 27),
        3: KeypadButton(MCP26, pin = 7, led_id = 28),
        4: KeypadButton(MCP26, pin = 1, led_id = 16),
        5: KeypadButton(MCP26, pin = 2, led_id = 25),
        6: KeypadButton(MCP27, pin = 1, led_id = 30),
        7: KeypadButton(MCP26, pin = 5, led_id = 18),
        8: KeypadButton(MCP27, pin = 2, led_id = 23),
        9: KeypadButton(MCP27, pin = 3, led_id = 32),
        0: KeypadButton(MCP26, pin = 0, led_id = 21),
        'input': KeypadButton(MCP27, pin = 7, led_id = 20),
        'ok': KeypadButton(MCP26, pin = 4, led_id = 34),
      },
      displays = [
        SevenSegment(peripherals.ARRAY, {
          'dot': 4,
          'top': 31,
          'left_top': 29,
          'left_bottom': 1,
          'right_top': 28,
          'right_bottom': 0,
          'middle': 11,
          'bottom': 14,
          }),
        SevenSegment(peripherals.ARRAY, {
          'dot': 22,
          'top': 15,
          'left_top': 2,
          'left_bottom': 13,
          'right_top': 21,
          'right_bottom': 27,
          'middle': 5,
          'bottom': 9,
          }),
        SevenSegment(peripherals.ARRAY, {
          'dot': 12,
          'top': 10,
          'left_top': 24,
          'left_bottom': 3,
          'right_top': 26,
          'right_bottom': 6,
          'middle': 30,
          'bottom': 25,
          }),
      ],
    ),
    'actions': {"%03d" % n: "Set course to %d!" % n for n in xrange(999)}
	},
]

disabled_controls = [
  {
    'id': 'throttle',
    'control': Throttle(first_led_id=37, led_count=15),
    'actions': {
      'low': 'Set throttle to minimum',
      'mid': 'Set throttle to medium',
      'high': 'Set throttle to maximum',
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
