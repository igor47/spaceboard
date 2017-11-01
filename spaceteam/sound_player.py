#!/usr/bin/env python
"""Functionality to play sounds in response to events"""

import glob
import os
import pyaudio
import Queue
import threading
import time
import wave

class _Sound(object):
  """container for sound files"""
  def __init__(self, path):
    self.wf = wave.open(path, 'rb')

class Mixer(threading.Thread):
  CHUNKSIZE = 1024

  def __init__(self):
    threading.Thread.__init__(self, name = 'player_mixer')
    self.setDaemon(True)
    self._queue = Queue.Queue(0)
    self.pyaudio = pyaudio.PyAudio()
    self._stop = threading.Event()

  def stop(self, final_sound = None):
    self._stop.set()
    self.join()
    if final_sound:
        self._play(final_sound)

    self.pyaudio.terminate()

  def run(self):
    while not self._stop.isSet():
      try:
        sound = self._queue.get(block=False, timeout=0.1)
        self._play(sound)
      except Queue.Empty:
        pass

  def queue(self, sound):
    self._queue.put(sound)

  def _play(self, sound):
    stream = self.pyaudio.open(
        format=self.pyaudio.get_format_from_width(sound.wf.getsampwidth()),
        channels=sound.wf.getnchannels(),
        rate=sound.wf.getframerate(),
        output=True)
    stream.start_stream()
    sound.wf.rewind()
    data = sound.wf.readframes(Mixer.CHUNKSIZE)
    while data != '':
      stream.write(data)
      data = sound.wf.readframes(Mixer.CHUNKSIZE)
    stream.close()

class SoundPlayer(object):
  def __init__(self):
    self.mixer = Mixer()

    src_dir = os.path.dirname(__file__)
    sound_dir = os.path.abspath(os.path.join(src_dir, '../sounds'))
    all_sounds = os.path.join(sound_dir, '*.wav')
    self.sounds = dict(
        (os.path.basename(name)[:-4], _Sound(name)) for name in glob.glob(all_sounds))

  def reset(self):
    self.mixer.start()

  def play(self, name):
    self.mixer.queue(self.sounds[name])

  def stop(self, final_sound = None):
    self.mixer.stop(final_sound)
    self.mixer.join()

if __name__ == "__main__":
    mixer = Mixer()
    mixer.start()
    mixer.queue(SoundPlayer.SOUNDS['startup'])
    time.sleep(2)
    mixer.stop()
