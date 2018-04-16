#!/usr/bin/env python2.7

from spaceteam import peripherals
peripherals.toggle_reset()
peripherals.DISPLAY.reset()

import time

while True:
  peripherals.DISPLAY.message = 'Unix time is %s' % time.time()
  peripherals.DISPLAY.communicate()
