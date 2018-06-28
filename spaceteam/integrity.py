#!/usr/bin/env python2.7

import time

class Integrity(object):
  """Displays hull integrity"""
  def __init__(self, microcontroller, array, leds):
    self.micro = microcontroller
    self.array = array
    self.leds = leds

    self.value = 100
    self.last_value = None

  def communicate(self):
    if self.value != self.last_value:
      self.last_value = self.value
      self.micro.set_oxygen(self.value)

      if self.value > 70:
        on = self.leds[0]
      elif self.value > 40:
        on = self.leds[1]
      else:
        on = self.leds[2]

      for led in self.leds:
        if led == on:
          self.array.turn_on(led)
        else:
          self.array.turn_off(led)

  def update(self, val):
    if val < 0 or val > 100:
      raise ValueError("integrity value must be between 0 and 100 (got %s)" % val)
    else:
      self.value = val

if __name__ == "__main__":
  import peripherals
  peripherals.reset_all()

  time.sleep(1)

  itg = peripherals.INTEGRITY
  for i in xrange(100):
    itg.update(100 - i)
    itg.communicate()
    itg.array.communicate()

    time.sleep(0.1)
