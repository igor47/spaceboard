from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

class SSD1306(object):
  def __init__(self, smbus, address = 0x3c):
    self.smbus = smbus
    self.address = address

    self.text = "Welcome!"

  def reset(self):
    with self.smbus.lock_grabber():
      self.device.show()

  def comms(self):
    with self.smbus.lock_grabber():
      with canvas(self.device) as draw:
        draw.rectangle(self.device.bounding_box, outline="white", fill="black")
        draw.text((10, 40), self.text, fill="white")
