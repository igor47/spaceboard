#!/usr/bin/env python2.7
"""Seven segment displays over the LED array

Accepts:
  array: an LedArray object
  pins: a mapping from pin descriptor (like 'top_right') to it's idx in the array
"""

import time

class SevenSegment(object):
  CHARS = {
      '1': ['right_top', 'right_bottom'],
      '2': ['top', 'right_top', 'middle', 'left_bottom', 'bottom'],
      '3': ['top', 'right_top', 'middle', 'right_bottom', 'bottom'],
      '4': ['left_top', 'right_top', 'middle', 'right_bottom'],
      '5': ['top', 'left_top', 'middle', 'right_bottom', 'bottom'],
      '6': ['left_top', 'left_bottom', 'middle', 'bottom', 'right_bottom'],
      '7': ['top', 'right_top', 'right_bottom'],
      '8': ['top', 'middle', 'bottom', 'right_top', 'right_bottom', 'left_top', 'left_bottom'],
      '9': ['top', 'middle', 'right_top', 'left_top', 'right_bottom'],
      '0': ['top', 'bottom', 'right_top', 'right_bottom', 'left_top', 'left_bottom'],
      'h': ['left_top', 'left_bottom', 'middle', 'right_bottom'],
      'a': ['left_bottom', 'left_top', 'middle', 'top', 'right_top', 'right_bottom'],
      'b': ['left_top', 'left_bottom', 'middle', 'bottom', 'right_bottom'],
      'c': ['top', 'middle', 'left_top', 'left_bottom'],
      'd': ['top', 'bottom', 'right_top', 'right_bottom', 'left_top', 'left_bottom'],
      'e': ['top', 'middle', 'bottom', 'left_top', 'left_bottom'],
      'f': ['top', 'middle', 'left_top', 'left_bottom'],
      '.': ['dot']
      }

  def __init__(self, array, pins):
    self.array = array
    self.pins = pins
    self.all_segments = set(self.pins.keys())

  def display(self, char):
    cannonical = str(char).lower()
    current = self.CHARS[cannonical]

    to_turn_off = self.all_segments - set(current)
    for segment in to_turn_off:
      idx = self.pins[segment]
      self.array.turn_off(idx)

    for segment in current:
      idx = self.pins[segment]
      self.array.turn_on(idx)

if __name__ == "__main__":
  import peripherals
  peripherals.reset_all()

  s1 = SevenSegment(peripherals.ARRAY, {
    'dot': 4,
    'top': 31,
    'left_top': 29,
    'left_bottom': 1,
    'right_top': 28,
    'right_bottom': 0,
    'middle': 11,
    'bottom': 14,
    })

  s2 = SevenSegment(peripherals.ARRAY, {
    'dot': 22,
    'top': 15,
    'left_top': 2,
    'left_bottom': 13,
    'right_top': 21,
    'right_bottom': 27,
    'middle': 5,
    'bottom': 9,
    })

  s3 = SevenSegment(peripherals.ARRAY, {
    'dot': 12,
    'top': 10,
    'left_top': 24,
    'left_bottom': 3,
    'right_top': 26,
    'right_bottom': 6,
    'middle': 30,
    'bottom': 25,
    })

  time.sleep(5)

  s1.display('h')
  s2.display('e')
  s3.display('1')
  peripherals.ARRAY.communicate()
  time.sleep(5)

  s1.display('e')
  s2.display('1')
  s3.display('1')
  peripherals.ARRAY.communicate()
  time.sleep(5)

  s1.display('1')
  s2.display('1')
  s3.display('0')
  peripherals.ARRAY.communicate()
  time.sleep(5)

  s1.display('1')
  s2.display('0')
  s3.display('.')
  peripherals.ARRAY.communicate()
  time.sleep(5)

  s1.display('1')
  s2.display('0')
  s3.display('.')
  peripherals.ARRAY.communicate()
  time.sleep(5)

  s1.display('0')
  s2.display('.')
  s3.display('.')
  peripherals.ARRAY.communicate()
  time.sleep(5)

  s1.display('.')
  s2.display('.')
  s3.display('.')
  peripherals.ARRAY.communicate()
  print "moving on!"
