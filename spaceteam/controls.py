#!/usr/bin/env python2.7
"""
The collection of our various types of controls
"""

import peripherals
from colour import Color
import time

class Switch(object):
  def __init__(self, device, pin, sounds = None):
    self.device = device
    self.pin = pin
    self.sounds = sounds

    self.prev_value = None
    self.value = None

  def active(self):
    """is the switch currently switched?"""
    # invert -- we use pull-up resistors, so an ON switch is low
    return not self.value

  def read(self):
    self.prev_value = self.value
    self.value = self.device.read(self.pin)
    self.play_sound()

    self.after_read()

  def play_sound(self):
    if self.prev_value != self.value:
      try:
        sound = self.sounds[self.value]
      except:
        pass
      else:
        peripherals.SOUNDS.play(sound)

  def after_read(self):
    pass

class SwitchWithPulldown(Switch):
  """Like a normal switch, but disables the pull-up on an MCP"""
  def __init__(self, device, pin, sounds = None):
    Switch.__init__(self, device, pin, sounds)
    device.pullups[pin] = 0

class SwitchWithLight(Switch):
  ACTIVE_COLOR = Color("green")
  INACTIVE_COLOR = Color("orange")

  def __init__(self, device, pin, led_id, sounds = None):
    Switch.__init__(self, device, pin, sounds)

    self.led_id = led_id
    self.prev_color = None

  def after_read(self):
    Switch.after_read(self)
    self.set_color()

  def set_color(self):
    new_color = self.ACTIVE_COLOR if self.active() else self.INACTIVE_COLOR
    if self.prev_color != new_color:
      peripherals.MAPLE.set_led(self.led_id, new_color, latch = False)
      self.prev_color = new_color

class SwitchWithTwoLights(Switch):
  UP_ON_COLOR = Color(rgb = (0.8, 0.2, 0))
  UP_OFF_COLOR = Color(rgb = (0.1, 0.025, 0))

  DOWN_ON_COLOR = Color(rgb = (0, 0.2, 0.4))
  DOWN_OFF_COLOR = Color(rgb = (0, 0.025, 0.05))

  def __init__(self, device, pin, led_up_id, led_down_id, sounds = None):
    Switch.__init__(self, device, pin, sounds)
    self.led_up_id = led_up_id
    self.led_down_id = led_down_id

    self.prev_up_color = None
    self.prev_down_color = None

  def after_read(self):
    Switch.after_read(self)
    self.set_color()

  def set_color(self):
    up_color = self.UP_ON_COLOR if self.active() else self.UP_OFF_COLOR
    if up_color != self.prev_up_color:
      self.prev_up_color = up_color
      peripherals.MAPLE.set_led(self.led_up_id, up_color)

    down_color = self.DOWN_OFF_COLOR if self.active() else self.DOWN_ON_COLOR
    if down_color != self.prev_down_color:
      self.prev_down_color = down_color
      peripherals.MAPLE.set_led(self.led_down_id, down_color)

class SwitchWithLed(Switch):
  def __init__(self, device, pin, array_idx, sounds = None):
    Switch.__init__(self, device, pin, sounds)
    self.array_idx = array_idx
    self.led_state = None

  def after_read(self):
    Switch.after_read(self)
    self.set_color()

  def set_color(self):
    new_state = True if self.active() else False
    if self.led_state != new_state:
      peripherals.ARRAY.set_led(self.array_idx, new_state)
      self.led_state = new_state

class KeypadButton(SwitchWithLight):
  """Just like a switch with a light, but calls a callback on press"""

  def __init__(self, device, pin, led_id):
    SwitchWithLight.__init__(self, device, pin, led_id)
    self.callback = lambda btn: None

  def after_read(self):
    SwitchWithLight.after_read(self)
    if self.prev_value != self.value:
      self.callback(self)

class Keypad(object):
  """A keypad; this is pretty specific to my board"""
  REQUIRED_KEYS = set([0,1,2,3,4,5,6,7,8,9,'input','ok'])

  ACTIVE_COLOR = Color("green")
  INACTIVE_COLOR = Color("green", saturation = 0.5)

  DISABLED_COLOR = Color("orange")
  DISABLED_ACTIVE_COLOR = Color("red")

  BLINK_COLOR = Color("blue")
  BLINK_INTERVAL_SEC = 0.5

  def __init__(self, buttons, displays):
    # did we get the buttons we require?
    provided = set(buttons.keys())
    if provided != self.REQUIRED_KEYS:
      raise RuntimeError(
          "Keypad requires a dictionary of buttons with exactly keys %s, but %s was provided" % (
            self.REQUIRED_KEYS, provided))

    # save ref to displays
    self.displays = displays

    # save and initialize callbacks on key press
    self.buttons = buttons
    for label in self.buttons:
      self.buttons[label].callback = self.callback_for(label)

    # internal state
    self.next_blink = 0
    self.input_mode = False
    self.blink_on_mode = False

    # set colors on the buttons
    self.set_button_colors()

    # what should we be displaying right now?
    self.last_display = None
    self.display = ['H', 'E', 'H']
    self.value = 0

  def callback_for(self, label):
    return lambda btn: self.key_pressed(label, btn)

  def key_pressed(self, label, btn):
    # we only care about key press, not key release
    if not btn.active():
      return

    if label == 'input':
      if not self.input_mode:
        self.input_mode = True

    elif label == 'ok':
      if self.input_mode:
        self.input_mode = False
        self.value = "".join([str(s) for s in self.display])

    else:
      if self.input_mode:
        self.display = self.display[1:] + [label]

  def set_button_colors(self):
    """sets the colors for all the keys based on the current mode"""
    # in input mode, the number keys and the ok key are active
    if self.input_mode:
      # numbers are active (aka green)
      number_active_color = self.ACTIVE_COLOR
      number_inactive_color = self.INACTIVE_COLOR

      # input button is inactive
      self.buttons['input'].ACTIVE_COLOR = self.DISABLED_ACTIVE_COLOR
      self.buttons['input'].INACTIVE_COLOR = self.DISABLED_COLOR

      # the ok button is active and blinking
      self.buttons['ok'].ACTIVE_COLOR = self.ACTIVE_COLOR
      if self.blink_on_mode:
        self.buttons['ok'].INACTIVE_COLOR = self.BLINK_COLOR
      else:
        self.buttons['ok'].INACTIVE_COLOR = self.INACTIVE_COLOR

    # otherwise, only the input key is active (and is blinking)
    else:
      # numbers are inactive
      number_active_color = self.DISABLED_ACTIVE_COLOR
      number_inactive_color = self.DISABLED_COLOR

      # ok button is inactive too
      self.buttons['ok'].ACTIVE_COLOR = self.DISABLED_ACTIVE_COLOR
      self.buttons['ok'].INACTIVE_COLOR = self.DISABLED_COLOR

      # the input button is active and blinking
      self.buttons['input'].ACTIVE_COLOR = self.ACTIVE_COLOR
      if self.blink_on_mode:
        self.buttons['input'].INACTIVE_COLOR = self.BLINK_COLOR
      else:
        self.buttons['input'].INACTIVE_COLOR = self.INACTIVE_COLOR

    # now we need to iterate through the number keys and set them
    for key in xrange(0, 10):
      btn = self.buttons[key]
      btn.ACTIVE_COLOR = number_active_color
      btn.INACTIVE_COLOR = number_inactive_color

  def read(self):
    # handle blinking
    now = time.time()
    if now > self.next_blink:
      self.next_blink = now + self.BLINK_INTERVAL_SEC
      self.blink_on_mode = not self.blink_on_mode

    # set the button colors based on the current mode
    self.set_button_colors()

    # make sure the display is correct
    self.set_display()

    # now lets read the inputs; that will set colors if necessary
    for btn in self.buttons.values():
      btn.read()

  def set_display(self):
    for idx, char in enumerate(self.display):
      d = self.displays[idx]
      d.display(char)

class Analog(object):
  CHANGE_THRESHOLD = 2

  """An analog input (potentiometer)"""
  def __init__(self, device, pin):
    self.device = device
    self.pin = pin

    # initialize hysterisis
    self.prev_value = 500
    self.value = 500

    # enable reading that pin
    self.device.enable_pin(pin)

  def read(self):
    cur_value = int(self.device.read(self.pin, scaled = True))

    # we only save the new value if it's changed more than threshold
    # this prevents oscillating due to analog jitter
    change = abs(cur_value - self.value)
    if change > self.CHANGE_THRESHOLD:
      self.prev_value = self.value
      self.value = cur_value

    self.after_read()

  def after_read(self):
    pass

class Accelerator(object):
  """A potentiometer with LEDs indicating the position"""
  RANGE = 50  # how high does it get?

  def __init__(self, device, pin, first_led_id, led_count):
    self.sensor = Analog(device, pin)

    self.value = None
    self.prev_value = None

    self.first_led_id = first_led_id
    self.led_count = led_count

    # configure the colors
    self.black = Color("black")
    self.color_range = [
        Color(rgb = (0, 0.02, 0)),
        Color(rgb = (0, 0.10, 0)),
        Color(rgb = (0, 0.15, 0)),
        Color(rgb = (0, 0.20, 0)),
        Color(rgb = (0, 0.35, 0)),

        Color(rgb = (0, 0.40, 0.05)),
        Color(rgb = (0, 0.55, 0.10)),
        Color(rgb = (0, 0.65, 0.15)),
        Color(rgb = (0, 0.70, 0.25)),
        Color(rgb = (0, 0.75, 0.30)),

        Color(rgb = (0.10, 0.60, 0.20)),
        Color(rgb = (0.25, 0.50, 0.10)),
        Color(rgb = (0.40, 0.40, 0.05)),
        Color(rgb = (0.60, 0.30, 0)),
        Color(rgb = (0.70, 0.20, 0)),

        Color(rgb = (0.80, 0.10, 0)),
        Color(rgb = (0.90, 0.05, 0)),
      ]

  def read(self):
    self.sensor.read()
    pct = float(self.sensor.value) / self.RANGE

    self.prev_value = self.value
    self.value = int(self.led_count * pct)
    self.set_leds()
    self.set_music()

  def set_leds(self):
    """loads the attached led string with the correct colors"""
    if self.value == self.prev_value:
      pass

    cur_color = self.color_range[self.value]

    new_colors = [cur_color] * self.value     # these leds are on
    new_colors += [self.black] * (self.led_count - self.value) # these are off

    peripherals.MAPLE.set_led_batch(self.first_led_id, new_colors[::-1])

  def set_music(self):
    pass

class RotaryEncoder(object):
  """A rotary encoder!"""
  pass

class HandScanner(object):
  """Pretends to be a hand scanner, but really just temperature"""
  pass
