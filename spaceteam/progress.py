#!/usr/bin/python

from colour import Color

LED_COUNT = 15
FIRST_LED = 46

class Progress(object):
  """Shows the remaining time..."""

  def __init__(self, micro, led_count = LED_COUNT, first_led = FIRST_LED):
    self.micro = micro
    self.led_count = led_count
    self.first_led = first_led

    self.prev_pct = None
    self.pct = 0

    self.black = Color("black")
    self.color_range = [
        Color(rgb = (1, 0, 0)),
        Color(rgb = (0.95, 0.02, 0)),
        Color(rgb = (0.90, 0.05, 0)),
        Color(rgb = (0.80, 0.08, 0)),
        Color(rgb = (0.75, 0.10, 0)),
        Color(rgb = (0.70, 0.15, 0)),
        Color(rgb = (0.60, 0.20, 0)),

        Color(rgb = (0.50, 0.40, 0)),

        Color(rgb = (0.40, 0.45, 0)),
        Color(rgb = (0.30, 0.50, 0)),
        Color(rgb = (0.20, 0.55, 0)),
        Color(rgb = (0.15, 0.60, 0)),
        Color(rgb = (0.10, 0.70, 0)),
        Color(rgb = (0.05, 0.80, 0)),
        Color(rgb = (0, 0.90, 0)),
      ]

  def reset(self):
    self.write()

  def write(self):
    pct = self.pct

    # fpct should be a float between 0 and 1
    fpct = pct if pct < 1 else float(pct) / 100
    fpct = 100 if fpct > 100 else fpct
    fpct = 0 if fpct < 0 else fpct

    # what's the color and index of the last led on?
    color = self.color_range[int(fpct * len(self.color_range))]
    idx = int(self.led_count * fpct) + 1

    # set the colors
    new_colors = [color] * idx
    new_colors += [self.black] * (self.led_count - idx)
    self.micro.set_led_batch(self.first_led, new_colors[::-1])

    # save the pct we worked with
    self.prev_pct = pct

  def communicate(self):
    if self.prev_pct != self.pct:
      self.write()
