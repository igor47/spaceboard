#!/usr/bin/env python2.7

import spaceteam

from colour import Color
import sys
import timeA

def main(args):
  # load and initialize our peripherals
  from spaceteam import peripherals
  peripherals.reset_all()

  # begin looping over them, reading their state
  from spaceteam import peripheral_reader
  peripheral_reader.begin_reading(peripherals.ALL)

  # initialize local state
  from spaceteam import state
  prev_state = state.generate()

  # loop, generating new state each time
  while True:
    new_state = state.generate()

    # send any state updates
    # we should determine how the state has changed, or else send the whole thing
    pass

    # recieve any instructions from the network
    pass

if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
