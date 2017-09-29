#!/usr/bin/env python2.7

import spaceteam
from spaceteam import MCP23017
from spaceteam import ADS1115
from spaceteam import RPi
from spaceteam import Microcontroller

from colour import Color
import sys
import time

def main(args):
  pi = RPi()
  pi.reset_peripherals()

  mcp1 = MCP23017(0x20)
  mcp1.set_as_output(15)
  mcp1.set_as_output(14)

  mcp1.write(15, 1)
  time.sleep(0.5)
  mcp1.write(14, 1)
  time.sleep(0.5)
  mcp1.write(15, 0)
  time.sleep(0.5)
  mcp1.write(14, 0)

  analog = ADS1115(0x48)
  microcontroller = Microcontroller("/dev/serial0")

  starting_color = Color("blue")
  starting_color.set_luminance(0.1)
  ending_color = Color("orange")
  ending_color.set_luminance(0.8)
  c_range = list(starting_color.range_to(ending_color, 41))

  while True:
    v = int(analog.read(scaled = True))
    idx = v if v < len(c_range) else -1
    c = c_range[idx]
    count = (idx >> 1) + 1

    print "sending color idx %s (%s) for value %d" % (idx, c, v)
    microcontroller.set_led_batch(1, [c] * (count) + [Color("black")] * (20 - count))

  print args
  return 0

if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
