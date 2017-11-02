#!/usr/bin/env python
"""Functionality to play sounds in response to events"""

import glob
import pygame as pg
import os
import time

class SoundPlayer(object):
  def __init__(self):
    # init the mixer
    pg.mixer.init(
        frequency = 48000,
        size = -16,
        channels = 2,
        buffer = 4096,
      )
    pg.init()
    pg.mixer.set_num_channels(20)

    # find the sounds we have saved
    src_dir = os.path.dirname(__file__)
    sound_dir = os.path.abspath(os.path.join(src_dir, '../sounds'))
    all_sounds = os.path.join(sound_dir, '*.wav')
    self.sounds = dict((os.path.basename(name)[:-4], name) for name in glob.glob(all_sounds))

    # thread management
    self.channels = []

  def reset(self):
    "nothing to do here"
    pass

  def stop(self):
    while len(self.channels) > 0:
      for channel in self.channels:
        if not channel.get_busy():
          self.channels.remove(channel)

      time.sleep(0.1)

  def play(self, name, volume = None):
    sound = pg.mixer.Sound(self.sounds[name])
    if volume:
      sound.set_volume(volume)

    self.channels.append(sound.play())

  def set_music(self, name, volume = 0.3):
    if name is None:
      pg.mixer.music.fadeout(1)
    else:
      pg.mixer.music.load(self.sounds[name])
      pg.mixer.music.play(-1)
      if volume:
        pg.mixer.music.set_volume(volume)

if __name__ == "__main__":
  p = SoundPlayer()
  p.play('space')
  p.stop()
