from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import ImageFont
import os
import textwrap
import time

from utils import *

class SSD1306(object):
  FONT = 'inconsolata.ttf'
  FONT_SIZE = 12
  STATUS_TIME_SEC = 2 # how long to display status messages

  def __init__(self, smbus, address = 0x3c):
    self.smbus = smbus
    self.address = address
    self.device = None

    self.prev_message = None
    self.message = "Initializing navigation...."

    self.status = None
    self.status_expires = None

    self.font = self.get_font(self.FONT, self.FONT_SIZE)

  def __str__(self):
    return "<SSD1306 at {:x}>".format(self.address)

  def get_font(self, name, size):
    src_dir = os.path.dirname(__file__)
    font_dir = os.path.abspath(os.path.join(src_dir, '../fonts'))
    font_path = os.path.join(font_dir, name)
    return ImageFont.truetype(font_path, size)

  def reset(self):
    self.device = ssd1306(bus = self.smbus, address = self.address)
    self.device.show()
    self._write()

  def communicate(self):
    if self.prev_message != self.message:
      self._write()

  @retry_i2c
  def _write(self):
    # we have an unexpired status -- leave it on the screen
    if self.status_expires and time.time() < self.status_expires:
      return

    with canvas(self.device) as draw:
      # clear the screen by drawing a box over everything
      draw.rectangle(self.device.bounding_box, outline="white", fill="black")

      # figure out what text to draw
      if self.status:
        self._draw_text(draw, self.status)
        self.status = None
        self.prev_message = None
        self.status_expires = time.time() + self.STATUS_TIME_SEC

      # we should draw the current message
      else:
        self.status_expires = None
        self.prev_message = self.message
        self._draw_text(draw, self.message)

  def _draw_text(self, draw, text):
    """Actually draw the text on the screen"""
    lines = textwrap.wrap(text, 18)

    y = 7
    for line in lines:
      draw.text((8, y), line, fill="white", font=self.font)
      y += 14
