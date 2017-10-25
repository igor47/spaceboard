from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

class SSD1306(object):
  def __init__(self, address = 0x3c):
    self.serial = i2c(port = 1, address = address)
    self.device = ssd1306(self.serial)

    self.device.show()

  def show_rotary(self, value, direction):
    with canvas(self.device) as draw:
      draw.rectangle(self.device.bounding_box, outline="white", fill="black")
      draw.text((10, 40), "Rotary encoder: %s" % value, fill="white")
