from luma.core.interface.serial import spi
from luma.oled.device import ssd1325

from utils import *

from display import Display

class SSD1325(Display):
  def __init__(self, gpio, gpio_DC, gpio_RESET, port = 0, device = 0):
    Display.init(self)

    self.port = port
    self.device = device
    self.spi = spi(
        gpio = gpio,
        port = self.port,
        device = self.device,
        gpio_DC = gpio_DC,
        gpio_RESET = gpio_RESET)

    self.device = self.get_device()

  def __str__(self):
    return "<SSD1323 at SPI{:x}:{:x}>".format(self.port, self.device)

  def get_device(self):
    return ssd1325(self.spi)
