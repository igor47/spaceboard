#!/usr/bin/env python2.7

from spaceteam.microcontroller import Microcontroller
m = Microcontroller('/dev/serial0')

from colour import Color
import time

def blink():
  m.set_led_batch(0, [Color(red = 0.1)] * 45)
  time.sleep(0.5)
  m.set_led_batch(0, [Color(green = 0.1)] * 45)
  time.sleep(0.5)

while True:
  blink()
