from luma.core.render import canvas

from PIL import ImageFont
import os
import textwrap
import time

from utils import *

class Display(object):
  FONT = 'inconsolata.ttf'
  FONT_SIZE = 12
  STATUS_TIME_SEC = 2 # how long to display status messages

  def __init__(self):
    self.prev_message = None
    self.message = "Initializing navigation...."

    self.status = None
    self.status_expires = None

    self.font = self.get_font(self.FONT, self.FONT_SIZE)

    # initialize in subclasses
    self.device = None

  def get_font(self, name, size):
    src_dir = os.path.dirname(__file__)
    font_dir = os.path.abspath(os.path.join(src_dir, '../fonts'))
    font_path = os.path.join(font_dir, name)

    _, ext = os.path.splitext(name)
    if ext == 'ttf':
      return ImageFont.truetype(font_path, size)
    else:
      return ImageFont.load(font_path)

  def reset(self):
    self.device = self.get_device()
    self.device.show()
    self._write()

  def get_device(self):
    """provide in sub-classes to initialize the device"""
    return None

  def communicate(self):
    if self.prev_message != self.message:
      self._write()

  def _write(self):
    # we have an unexpired status -- leave it on the screen
    if self.status_expires and time.time() < self.status_expires:
      return

    with canvas(self.device) as draw:
      draw.fontmode = "1"

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
