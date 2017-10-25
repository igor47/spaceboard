import threading
from time import sleep

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class Rotary(object):
  def __init__(self, pin_a, pin_b, on_change = None):
    self.pin_a = pin_a
    self.pin_b = pin_b

    self.on_change = on_change

    # state
    self.counter = 0

    # pins are inputs
    GPIO.setup(self.pin_a, GPIO.IN, GPIO.PUD_OFF)
    GPIO.setup(self.pin_b, GPIO.IN, GPIO.PUD_OFF)

    # get state
    self.prev_a = GPIO.input(self.pin_a)
    self.prev_b = GPIO.input(self.pin_b)

    # set callbacks
    self.rotary1_cb = GPIO.add_event_detect(self.pin_a, GPIO.BOTH, self.pulse)
    self.rotary1_cb = GPIO.add_event_detect(self.pin_b, GPIO.BOTH, self.pulse)

  def pulse(self, pin):
    cur_a = GPIO.input(self.pin_a)
    cur_b = GPIO.input(self.pin_b)

    # remove duplicates
    if cur_a == self.prev_a and cur_b == self.prev_b:
      return
    else:
      self.prev_a = cur_a
      self.prev_b = cur_b

    # only pay attention to 1-1 states
    if not cur_a or not cur_b:
      return

    if pin == self.pin_a:
      direction = 1
    else:
      direction = -1

    self.counter += direction
    if self.on_change:
      self.on_change(self.counter, direction)
