#!/usr/bin/env python2.7

from spaceteam import peripherals
peripherals.reset_all()

import time

m = peripherals.MCP27
while True:
  m.read_inputs()
  print m.input_latches

  time.sleep(0.1)
