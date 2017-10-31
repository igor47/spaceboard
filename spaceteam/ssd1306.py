from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import ImageFont
import os

class SSD1306(object):
  FONT = 'inconsolata.ttf'
  FONT_SIZE = 10

  def __init__(self, smbus, address = 0x3c):
    self.smbus = smbus
    self.device = ssd1306(bus = self.smbus, address = address)

    self.prev_text = None
    self.text = "Welcome!"

    self.font = self.get_font(self.FONT, self.FONT_SIZE)

  def font(self, name, size):
    src_dir = os.path.dirname(__file__)
    font_dir = os.path.abspath(os.path.join(src_dir, '../fonts'))
    font_path = os.path.join(font_dir, name)
    return ImageFont.truetype(font_path, size)

  def reset(self):
    with self.smbus.lock_grabber():
      self.device.show()

  def communicate(self):
    if self.prev_text != self.text:
      self.write_text()

  def write_text(self):
    # write whatever text is at the beginning of the function
    # if it changes while this is running, we'll do another write
    to_write = self.text

    # do the writing
    with self.smbus.lock_grabber():
      with canvas(self.device) as draw:
        draw.rectangle(self.device.bounding_box, outline="white", fill="black")
        draw.text((10, 40), to_write, fill="white", font = self.font)

        # save what we wrote
        self.prev_text = to_write
