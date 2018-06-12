#!/usr/bin/env python2.7

import time

from spaceteam import peripherals
peripherals.reset_all()

devs = [dev for dev in peripherals.INPUTS if type(dev) is peripherals.MCP23017]

for dev in devs:
  dev.communicate()

old = [dev.input_latches for dev in devs]

while True:
  for dev_idx in xrange(len(devs)):
    dev = devs[dev_idx]
    dev.communicate()

    prev = old[dev_idx]
    new = dev.input_latches

    for idx, val in enumerate(new):
      if prev[idx] != val:
        print "on %s, val %d has changed from %d to %d" % (dev, idx, prev[idx], val)

    old[dev_idx] = new

  time.sleep(0.1)
