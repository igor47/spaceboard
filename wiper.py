#!/usr/bin/env python2.7

import time

from spaceteam import peripherals
leds = peripherals.LEDS

while True:
  leds.wipe()
  print "wiped!"
