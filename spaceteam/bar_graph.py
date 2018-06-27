#!/usr/bin/env python2.7
"""A little bar graph of LEDs on the array"""

import time

class BarGraph(object):
  """Displays the given value on a bar of 10 LEDs on an ARRAY

    Passed values:
      array: the array that the LEDs are on
      pins: a list of array idx values, [0] is the first led, [9] is the last
      mode: the mode (see below)

    Values: 0 means all LEDs are off, 10 means they're all on
    Modes:
      display: just displays the specified value
      countdown: display the specified value, but blink the last-lit LED
      sweep: a demo pattern which just runs several LEDs up the graph
  """
  MODES = [
      'display',
      'countdown',
      'sweep',
      ]

  BLINK_INTERVAL = 0.1 # in seconds
  SWEEP_WIDTH = 1

  def __init__(self, array, pins, mode = 'countdown'):
    self.array = array
    self.pins = pins
    self.mode = mode

    self.value = 0

    self._blink_time = 0
    self._blink_on = True

  def update_value(self, new_value):
    if new_value < 0 or new_value > 10:
      raise ValueError('BarGraph value must be between 0 and 10 (got %d)' % new_value)
    else:
      self.value = new_value

  def communicate(self):
    should_be_on = []

    if self.mode == 'sweep':
      # go up one led, and turn that one on
      self.update_value((self.value + 1) % 10)
      should_be_on = [self.value]

      # also turn on the leds below the current, specified by width
      for i in xrange(self.SWEEP_WIDTH):
        should_be_on.append((self.value - 1) % 10)

    elif self.mode in ['display', 'countdown']:
      # turn on all the leds up to value
      should_be_on = [i for i in xrange(10) if i < self.value]

      # if we're blinking, the last-on led should blink
      if self.mode == 'countdown':
        # manipulate internal blink state
        if time.now() > self._blink_time + self.BLINK_INTERVAL:
          self._blink_time = time.now()
          self._blink_on = not self._blink_on

        # turn the blinking led on/off
        blinking_idx = min(9, value)
        if self.countdown_blink_on:
          should_be_on.append(blinking_idx)
        else:
          should_be_on.remove(blinking_idx)

    else:
      raise ValueError('Invalid mode %s' % self.mode)

    for idx, pin in enumerate(self.pins):
      if idx in should_be_on:
        self.array.turn_on(pin)
      else:
        self.array.turn_off(pin)

if __name__ == "__main__":
  import peripherals
  peripherals.reset_all()

  while True:
    for bar in peripherals.BARS:
      bar.communicate()

    peripherals.ARRAY.communicate()
    time.sleep(0.5)
