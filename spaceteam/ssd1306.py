from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import ImageFont
import os
import textwrap

class SSD1306(object):
  FONT = 'inconsolata.ttf'
  FONT_SIZE = 12

  def __init__(self, smbus, address = 0x3c):
    self.smbus = smbus
    self.address = address
    self.device = None

    self.prev_message = None
    self.message = "Initializing navigation...."

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

  def _write(self):
    with canvas(self.device) as draw:
      draw.rectangle(self.device.bounding_box, outline="white", fill="black")

      # we've cleared the screen, now we write whatever is in our buffers
      msg = self.message
      lines = textwrap.wrap(msg, 18)

      y = 7
      for line in lines:
        draw.text((8, y), line, fill="white", font=self.font)
        y += 14

      self.prev_message = msg
