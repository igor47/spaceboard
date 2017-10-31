#!/usr/bin/env python2.7

import spaceteam
from spaceteam import Client
from spaceteam import PeripheralReader

from spaceteam import state

import time
import sdnotify

SERVER_IP = '10.110.0.1'

def comms(client, prev_state, new_state):
  diffs = {}
  for k in prev_state:
    if prev_state[k] != new_state[k]:
      diffs[k] = new_state[k]

  if diffs:
    print "diffs: %s" % diffs

  if not client:
    time.sleep(0.01)
    return

  # send any state updates
  # TODO: we should determine how the state has changed, or else send the whole thing
  client.send('announce', new_state)

  # recieve any instructions from the network
  message = client.read()
  if message is None:
    return

  if message['message'] == 'display':
    # TODO: we should display on some sort of peripheral
    print "we got a message from the server! %s" % message['data']

def main(args):
  # load and initialize our peripherals
  from spaceteam import peripherals
  peripherals.reset_all()

  # begin looping over them, reading their state
  client = None
  try:
    PeripheralReader.begin_reading(peripherals.ALL)
    time.sleep(1) # give some reader loops

    # initialize local state
    prev_state = state.generate()

    # initialize client connection
    if '--local' in args:
      print "Acting in local mode!"
    else:
      client = Client()
      client.connect(SERVER_IP)
      client.send('announce', prev_state)

    # initialize systemd notifications
    notifier = sdnotify.SystemdNotifier()
    notifier.notify("READY=1")

    # loop, generating new state each time
    while True:
      new_state = state.generate()
      comms(client, prev_state, new_state)
      prev_state = new_state

      notifier.notify("WATCHDOG=1")

  finally:
    if client:
      client.stop()

    PeripheralReader.stop_reading()

# run spaceteam!
import sys
if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
