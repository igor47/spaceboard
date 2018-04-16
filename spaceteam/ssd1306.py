from luma.oled.device import ssd1306
from utils import *

from display import Display

class SSD1306(Display):
  def __init__(self, smbus, address = 0x3c):
    Display.init(self)

    self.smbus = smbus
    self.address = address
    self.device = self.get_device()

  def __str__(self):
    return "<SSD1306 at {:x}>".format(self.address)

  def get_device(self):
    return ssd1306(bus = self.smbus, address = self.address)
