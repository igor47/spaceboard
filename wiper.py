#!/usr/bin/env python2.7

from spaceteam.max6971 import MAX6971

LED_DATA_PIN = 33
LED_CLOCK_PIN = 35
LED_LATCH_PIN = 37

LEDS = MAX6971(LED_DATA_PIN, LED_CLOCK_PIN, LED_LATCH_PIN, count = 2)

while True:
  LEDS.wipe()
