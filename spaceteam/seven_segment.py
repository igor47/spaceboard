#!/usr/bin/env python2.7
"""Handles peripherals.MCP23017 I/O Expanders on the I2C bus

More info:
  http://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf
"""

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
      }

  def __init__(self, pins):
    self.pins = pins
    self.all_segments = set(self.pins.keys())

  def display(self, char):
    cannonical = str(char).lower()
    current = self.CHARS[cannonical]

    to_turn_off = self.all_segments - set(current)
    for off in to_turn_off:
      self.set_state(off, 0)

    for on in current:
      self.set_state(on, 1)

  def set_state(self, segment, val):
    device, pin = self.pins[segment]
    device.set_as_output(pin)
    device.write(pin, val)

if __name__ == "__main__":
  import peripherals
  peripherals.reset_all()

  peripherals.MCP22.set_as_output(8)
  peripherals.MCP22.write(8, 1)
  peripherals.MCP22.communicate()

  s = SevenSegment({
    'dot': (peripherals.MCP22, 8),
    'top': (peripherals.MCP23, 2),
    'left_top': (peripherals.MCP22, 11),
    'left_bottom': (peripherals.MCP23, 11),
    'right_top': (peripherals.MCP23, 3),
    'right_bottom': (peripherals.MCP23, 12),
    'middle': (peripherals.MCP23, 8),
    'bottom': (peripherals.MCP23, 13),
    })
  s.display(3)

  peripherals.MCP22.communicate()
  peripherals.MCP23.communicate()
  print "displayed!"
  import time
  time.sleep(10)
  print "moving on!"

  peripherals.MCP22.set_as_output(8)
  peripherals.MCP22.write(8, 1)
  peripherals.MCP22.communicate()

