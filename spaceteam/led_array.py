#!/usr/bin/env python2.7
"""Handles an array of leds on MAX6971 shift registers attached to microcontroller

More info:
  https://datasheets.maximintegrated.com/en/ds/MAX6971.pdf

TODO: we could probably just use the pi for this instead of mediating through
the microcontroller...
"""

from ctypes import c_ubyte
import time

class LedArray(object):
  INSIDE_LED_PIN = 7

  def __init__(self, microcontroller, chip_count = 1):
    self.microcontroller = microcontroller
    self.chip_count = chip_count

    # we have two bytes per chip (8 outputs per chip)
    self.is_on = bytearray([0] * chip_count * 2)

    # we have some leds inside; lets use them to count main loops
    self.inside_led_on = 0

  def turn_on(self, idx):
    byte, bit = self.__idx_to_byte_bit(idx)
    self.is_on[byte] |= bit

  def turn_off(self, idx):
    byte, bit = self.__idx_to_byte_bit(idx)
    self.is_on[byte] &= c_ubyte(~bit).value

  def set_led(self, idx, on):
    if on:
      self.turn_on(idx)
    else:
      self.turn_off(idx)

  def toggle(self, idx):
    byte, bit = self.__idx_to_byte_bit(idx)
    active = (self.is_on[byte] & bit) != 0
    self.set_led(idx, not active)

  def communicate(self):
    """Reads the state of all enabled pins and saves it locally"""
    self.__advance_inside_leds()
    self.microcontroller.update_array(list(self.is_on))

  def __advance_inside_leds(self):
    """basically, a binary clock showing loop iterations"""
    # add one to the clock, wrapping if necessary
    self.inside_led_on += 1
    self.inside_led_on %= (1 << self.chip_count)

    # turn the value into a string of bits, one for each LED
    inside_bits = format(self.inside_led_on, '0%db' % self.chip_count)

    # turn each of those leds on/off
    for chip in range(self.chip_count):
      inside_idx = self.INSIDE_LED_PIN + (16 * chip)
      if inside_bits[chip] == '1':
        self.turn_on(inside_idx)
      else:
        self.turn_off(inside_idx)

  def __idx_to_byte_bit(self, idx):
    """returns the idx of the byte and a byte with the correct bit set to 1"""
    if idx >= self.chip_count * 16:
      raise ValueError(
          "Index %d is beyond the range of array of length %d" % (idx, self.chip_count))

    return (idx >> 3, 1 << (idx % 8))

if __name__ == "__main__":
  import peripherals
  peripherals.reset_all()

  array = peripherals.ARRAY

  idx = 0
  while True:
    array.turn_on(idx)
    array.communicate()
    raw_input("turned on %s; press <Enter> to continue..." % idx)

    array.turn_off(idx)
    idx = (idx + 1) % (16 * array.chip_count)
