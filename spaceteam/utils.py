"""Utilities for dealing with bits and bytes"""

ACCEPTABLE_BITS = [0, 1]
def bitlist_to_int(bitlist):
  out = 0
  for bit in bitlist:
    if not bit in ACCEPTABLE_BITS:
      raise RuntimeError("bit %s in bitlist %s is not valid!" % (bit, bitlist))

    out = (out << 1) | bit

  return out

def retry_i2c(func):
  def wrapper(*args, **kwargs):
    tries = 0
    while tries < 3:
      tries += 1
      try:
        return func(*args, **kwargs)
      except IOError, e:
        print "retrying on io error %s for the %s time" % (e, tries)

  return wrapper
