#!/usr/bin/env python2.7

import spaceteam
from spaceteam import Client

SERVER_IP = '10.110.0.1'

def main(args):
  # initialize client connection
  client = Client()
  client.connect(SERVER_IP)

  # load and initialize our peripherals
  from spaceteam import peripherals
  peripherals.reset_all()

  # begin looping over them, reading their state
  from spaceteam import peripheral_reader
  peripheral_reader.begin_reading(peripherals.ALL)

  # initialize local state
  from spaceteam import state
  prev_state = state.generate()

  # announce ourselves to the server
  client.send('announce', prev_state)

  # loop, generating new state each time
  while True:
    new_state = state.generate()

    # send any state updates
    # TODO: we should determine how the state has changed, or else send the whole thing
    client.send('announce', new_state)
    prev_state = new_state

    # recieve any instructions from the network
    message = client.read()
    if message is None:
      continue

    # act on any messages recieved
    if message['message'] == 'reset':
      pass

    if message['message'] == 'display':
      # TODO: we should display on some sort of peripheral
      print "we got a message from the server! %s" % message['data']

# run spaceteam!
import sys
if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
