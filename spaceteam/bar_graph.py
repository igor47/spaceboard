#!/usr/bin/env python2.7
"""A little bar graph of LEDs on the array"""

import time

class BarGraph(object):
  """Displays the given value on a bar of 10 LEDs on an ARRAY

    Passed values:
      array: the array that the LEDs are on
      pins: a list of array idx values, [0] is the first led, [-1] is the last
      mode: the mode (see below)

    Values: 0 means all LEDs are off, len(pins) means they're all on
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
  SWEEP_INTERVAL = 0.5 # in seconds
  SWEEP_WIDTH = 1

  def __init__(self, array, pins, mode = 'countdown'):
    self.array = array
    self.pins = pins
    self.mode = mode

    self.value = 0

    self._transition_time = 0
    self._blink_on = True

  def _time_for_transition(self, interval):
    t = time.time()
    if t > (self._transition_time + interval):
      self._transition_time = t
      return True
    else:
      return False

  def update_value(self, new_value):
    if new_value < 0 or new_value > len(self.pins):
      raise ValueError(
          'BarGraph value must be between 0 and %s (got %d)' % (len(self.pins), new_value))
    else:
      self.value = new_value

  def communicate(self):
    should_be_on = []

    if self.mode == 'sweep':
      # actually do the sweep
      if self._time_for_transition(self.SWEEP_INTERVAL):
        self.update_value((self.value + 1) % len(self.pins))

      # figure out which LEDs should be on based on value
      should_be_on = [self.value]
      for i in xrange(self.SWEEP_WIDTH):
        should_be_on.append((self.value - 1) % len(self.pins))

    elif self.mode in ['display', 'countdown']:
      # turn on all the leds up to value
      should_be_on = [i for i in xrange(len(self.pins)) if i < self.value]

      # if we're blinking, the last-on led should blink
      if self.mode == 'countdown':
        # manipulate internal blink state
        if self._time_for_transition(self.BLINK_INTERVAL):
          self._blink_on = not self._blink_on

        # turn the blinking led on/off
        blinking_idx = min(len(self.pins) - 1, self.value)
        if self._blink_on:
          should_be_on.append(blinking_idx)
        else:
          try:
            should_be_on.remove(blinking_idx)
          except ValueError:
            pass

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
