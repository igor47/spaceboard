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
    self.device = ssd1306(bus = self.smbus, address = address)

    self.prev_message = None
    self.message = "Hello World!"

    self.prev_status = None
    self.status = 0.5

    self.font = self.get_font(self.FONT, self.FONT_SIZE)

  def get_font(self, name, size):
    src_dir = os.path.dirname(__file__)
    font_dir = os.path.abspath(os.path.join(src_dir, '../fonts'))
    font_path = os.path.join(font_dir, name)
    return ImageFont.truetype(font_path, size)

  def reset(self):
    with self.smbus.lock_grabber():
      self.device.show()
      self._write()

  def communicate(self):
    if self.prev_message != self.message or self.prev_status != self.status:
      self._write()

  def _write(self):
    with self.smbus.lock_grabber():
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

        # now, write the status
        try:
          stat = float(self.status)
        except ValueError:
          stat = self.status
          draw.text((10, 40), stat, fill="white", font = self.font)
        else:
          width = int(self.device.width * stat)
          print "width is %s" % width
          box = (10, 40, 10 + width, 50)
          draw.rectangle(box, outline="white", fill="white")

        self.prev_status = stat
