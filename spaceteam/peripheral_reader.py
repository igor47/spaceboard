#!/usr/bin/env python2.7

"""
Handles reading peripheral input state. Each peripheral
stores the state locally.
"""

import threading
import time

# the actual reader code
class PeripheralReader(threading.Thread):
  # public API
  @classmethod
  def begin_reading(cls, prps):
    if cls.__READER:
      raise RuntimeError("A reader is already defined, can't begin reading twice!")
    else:
      cls.__READER = cls(prps)
      cls.__READER.start()

  @classmethod
  def stop_reading(cls):
    if cls.__READER:
      cls.__READER.stop()
      cls.__READER = None

  # private stuff
  __READER = None
  DEADLINE_SEC = 0.03  # we should read the peripherals this often

  def __init__(self, prps = []):
    threading.Thread.__init__(self, name = 'peripheral_reader')
    self.setDaemon(True)
    self._stop = threading.Event()

    self.peripherals = prps

  def stop(self):
    self._stop.set()
    self.join()

  def run(self):
    while not self._stop.isSet():
      deadline = time.time() + self.DEADLINE_SEC
      for p in self.peripherals:
        p.read_inputs()

      overrun_ms = (time.time() - deadline) * 1000
      if overrun_ms > 0:
        print "We took {0:0.3f} millis over deadline to read inputs".format(overrun_ms)
