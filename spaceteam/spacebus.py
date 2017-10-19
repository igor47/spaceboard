#!/usr/bin/env python2.7
"""
Our minimal wrapper around smbus provides a few utilities

The main goal is to provide a lock, so that the bus can safely be used from
threads by only one peripheral at at time
"""

import smbus

from contextlib import contextmanager
from threading import Lock

from errors import SMBUSTimeout

# we just hard-code this here for our project
BUS_ID = 1

# some constants for I2C
I2C_ALL_CALL = 0x0 # all call address -- goes to all devices (that support it)
I2C_SOFT_RESET = 0x06 # all devices reset

class Spacebus(smbus.SMBus):
  LOCK_TIMEOUT_SEC = 0.5

  def __init__(self):
    smbus.SMBus.__init__(self, BUS_ID)
    self.lock = Lock()

  def all_call_reset(self):
    with self.lock_grabber():
      self.i2c.write_byte(I2C_ALL_CALL, I2C_SOFT_RESET)

  @contextmanager
  def lock_grabber(self):
    locked = False
    give_up_time = time.time() + self.LOCK_TIMEOUT_SEC

    try:
      while True:
        locked = self.lock.aquire(False)
        if locked:
          yield True
          break

        if time.time() > give_up_time:
          raise SMBUSTimeout(
              "Gave up waiting for the SMBUS after %f seconds" % self.LOCK_TIMEOUT_SEC)

    finally:
      if locked:
        self.lock.release()


