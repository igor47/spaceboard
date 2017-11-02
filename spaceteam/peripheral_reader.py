#!/usr/bin/env python2.7

"""
Handles reading peripheral input state. Each peripheral
stores the state locally.
"""

import threading
import time

from spaceteam import peripherals

# the actual reader code
class PeripheralReader(threading.Thread):
  # public API
  @classmethod
  def begin_reading(cls):
    if len(cls.__THREADS) > 0:
      raise RuntimeError("Reader threads already started!")

    # a separate thread for dealing with microcontroller
    maple_prps = [peripherals.PROGRESS, peripherals.MAPLE]
    maple_thread = cls(maple_prps)
    maple_thread.start()
    cls.__THREADS.append(maple_thread)

    # thread for the rest of the stuff
    rest = peripherals.INPUTS + [peripherals.DISPLAY]
    rest_thread = cls(rest)
    rest_thread.start()
    cls.__THREADS.append(rest_thread)

    while not all([t.ran for t in cls.__THREADS]):
      time.sleep(0.1)

  @classmethod
  def stop_reading(cls):
    for t in cls.__THREADS:
      t.stop()
    cls.__THREADS = []

  @classmethod
  def running(cls):
    return all(t.is_alive() for t in cls.__THREADS)

  # private stuff
  __THREADS = []
  DEADLINE_MS = 30  # we should read the peripherals this often

  def __init__(self, prps = []):
    threading.Thread.__init__(self, name = 'peripheral_reader')
    self.setDaemon(True)
    self._stop = threading.Event()
    self.ran = False

    self.peripherals = prps

  def stop(self):
    self._stop.set()
    self.join()

  def run(self):
    while not self._stop.isSet():
      for p in self.peripherals:
        start = time.time()
        p.communicate()
        end = time.time()

        runtime_ms = (end - start) * 1000
        if runtime_ms > self.DEADLINE_MS:
          print "{1:06.2f} millis: {0:s}".format(p, runtime_ms)

      # notify that we finished at least one loop
      self.ran = True
