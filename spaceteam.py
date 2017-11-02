#!/usr/bin/env python2.7

import spaceteam
from spaceteam import Client
from spaceteam import PeripheralReader

from spaceteam import peripherals
from spaceteam import state

import time
import sdnotify

#SERVER_IP = '10.110.0.10'
SERVER_IP = '10.0.0.1'

def updates(prev, new):
  diffs = {}
  for k in prev:
    if prev[k] != new[k]:
      diffs[k] = new[k]

  return diffs

def main(args):
  # load and initialize our peripherals
  peripherals.reset_all()

  # begin looping over them, reading their state
  client = None
  try:
    # start communication with peripherals
    PeripheralReader.begin_reading()

    # initialize an announce message
    announce = state.announce()

    # initialize client connection
    if '--local' in args:
      print "Acting in local mode!"
    else:
      client = Client(SERVER_IP)
      client.start(announce)

    # initialize systemd notifications
    notifier = sdnotify.SystemdNotifier()
    notifier.notify("READY=1")

    # loop, generating new state each time
    prev_state = state.generate()
    while True:
      # check that everything is still working
      if client and not client.running():
        raise RuntimeError("The client has stopped!")
      if not PeripheralReader.running():
        raise RuntimeError("The peripheral reader has stopped!")

      # notify the watchdog that we're okay (otherwise we get rebooted)
      notifier.notify("WATCHDOG=1")

      # first, deal with any state updates
      new_state = state.generate()
      for id, val in updates(prev_state, new_state).items():
        if client:
          client.update(id, val)
        else:
          time.sleep(0.001)

      # update the state
      prev_state = new_state

      # deal with any messages from the server
      if not client:
        time.sleep(0.001)
        continue

      inst = client.get_instruction()
      while inst is not None:
        if inst['type'] == 'display':
          peripherals.DISPLAY.message = inst['message']

        elif inst['type'] == 'progress':
          peripherals.PROGRESS.pct = inst['message']

        #TODO: find some place to write the status
        elif inst['type'] == 'status':
          pass

        # get next instruction
        inst = client.get_instruction()

  finally:
    if client:
      client.stop()

    PeripheralReader.stop_reading()

# run spaceteam!
import sys
if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
