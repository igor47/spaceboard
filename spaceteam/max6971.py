#!/usr/bin/env python2.7
"""Handles MAX6971 family of led driving shift registers

More info:
  https://datasheets.maximintegrated.com/en/ds/MAX6971.pdf
"""

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

class MAX6971(object):
  def __init__(self, data, clock, latch, count = 1):
    self.data = data
    GPIO.setup(RESET_PIN, GPIO.OUT)
    self.clock = clock
    self.latch = latch

    # set all used pins as output and LOW
    for pin in [self.latch, self.clock, self.data]:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, 0)

    self.state = [0] * 16 * count

  def wipe(self):
    """wipes all the leds on, then off"""
    idx = len(self.state) - 1
    while idx >= 0:
      self.state[idx] = 1
      self.display()

    idx = len(self.state) - 1
    while idx >= 0:
      self.state[idx] = 0
      self.display()

  def display(self):
    """Writes the state in self.state to the LED array"""
    # make sure clock/latch are low to start (should already be the case)
    GPIO.output(self.clock, 0)
    GPIO.output(self.latch, 0)

    # write out all the data (bit banging!)
    for led in self.state[::-1]:
      GPIO.output(self.data, led)
      GPIO.output(self.clock, 1)
      GPIO.output(self.clock, 0)

    # toggle latch to display the data
    GPIO.output(self.latch, 1)
    GPIO.output(self.latch, 0)
