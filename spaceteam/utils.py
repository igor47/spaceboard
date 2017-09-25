"""Utilities for dealing with bits and bytes"""

ACCEPTABLE_BITS = [0, 1]
def bitlist_to_int(bitlist):
  out = 0
  for bit in bitlist:
    if not bit in ACCEPTABLE_BITS:
      raise RuntimeError("bit %s in bitlist %s is not valid!" % (bit, bitlist))

    out = (out << 1) | bit

  return out

