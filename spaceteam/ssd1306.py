from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

class SSD1306(object):
  def __init__(self, smbus, address = 0x3c):
    self.smbus = smbus
    self.device = ssd1306(bus = self.smbus, address = address)

    self.prev_text = None
    self.text = "Welcome!"

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
        draw.text((10, 40), to_write, fill="white")

        # save what we wrote
        self.prev_text = to_write
