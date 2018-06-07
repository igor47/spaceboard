#!/usr/bin/env python2.7

import time

from spaceteam.peripherals import MAPLE

while True:
  for i in xrange(80):
    MAPLE.set_array_led(i, 1)

  MAPLE.latch_leds()

  for i in xrange(80):
    MAPLE.set_array_led(i, 0)

  MAPLE.latch_leds()
  print "wiped!"
