#!/usr/bin/env python2.7

"""
Handles reading peripheral input state. Each peripheral
stores the state locally.
"""

# the public API is just these two functions
def begin_reading(prps):
  """starts the loop which reads the input state of the peripherals"""
  if not _READER:
    _READER = _PeripheralReader(prps)
    _READER.start()

def stop_reading():
  """stops the reader loop"""
  if _READER:
    _READER._stop()
    _READER = None

# the reader object -- a thread that constantly polls the peripherals
_READER = None

# the actual reader code
class _PeripheralReader(threading.Thread):
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

      overrun = time.time() - deadline
      if overrun > 0:
        print "We took {0:0.3f} microseconds over deadline to read inputs"
