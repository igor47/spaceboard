#!/usr/bin/env python2.7

from spaceteam import peripherals
peripherals.reset_all()

import time

m = peripherals.MCP25
m.communicate()
prev = m.input_latches

while True:
  m.communicate()
  for idx, val in enumerate(m.input_latches):
    if prev[idx] != val:
      print "val %d has changed from %d to %d" % (idx, prev[idx], val)

  prev = m.input_latches
  time.sleep(0.1)
