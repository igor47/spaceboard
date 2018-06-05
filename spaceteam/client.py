#!/usr/bin/env python2.7
"""
Acts as a client to a central control server
"""

import json
import socket
import struct
import threading
import time
import Queue

DEFAULT_PORT = 8000

class Client:
  """Handles communication with the server and polling state updates."""
  KEEPALIVE_THRESH_SEC = 10

  def __init__(self, host, port = DEFAULT_PORT):
    """initialize comms"""
    self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.host = host
    self.port = port

    self.read_buffer = ''

    self.recv_thread = None
    self.recv_stop = threading.Event()
    self.recv_events = Queue.Queue()

    self.last_keepalive = time.time()

  def start(self, announce):
    self._socket.connect((self.host, self.port))
    self._send('announce', {'controls': announce})

    # start the reader thread
    self.recv_thread = threading.Thread(target = self._reader)
    self.recv_thread.start()

  def stop(self):
    if self.recv_thread:
      self.recv_stop.set()
      self.recv_thread.join()

    self._socket.close()

  def update(self, id, value):
    self._send('set-state', {'id': id, 'state': str(value)})

  def get_instruction(self):
    try:
      return self.recv_events.get(block = False)
    except Queue.Empty:
      return None

  def running(self):
    recv_thread_alive = self.recv_thread and self.recv_thread.is_alive()
    keepalive_happening = (time.time() - self.last_keepalive) < self.KEEPALIVE_THRESH_SEC
    running = recv_thread_alive and keepalive_happening

    return running

  def _send(self, message, data):
    """encodes and sends a message to the server"""
    msg = self.encode({
      'message': message,
      'data': data,
      })
    self._socket.sendall(msg)

  def _reader(self):
    """performs the reading from the socket and handling messages"""
    def parse_msg(msg):
      if msg['message'] == 'set-display':
        return {'type': 'display', 'message': msg['data']['message']}

      elif msg['message'] == 'set-status':
        return {'type': 'status', 'message': msg['data']['message']}

      elif msg['message'] == 'set-progress':
        return {'type': 'progress', 'message': msg['data']['value']}

      elif msg['message'] == 'keep-alive':
        self.last_keepalive = time.time()

    while not self.recv_stop.isSet():
      self.read_buffer += self._socket.recv(4096)

      msg = self.pop_from_buffer()
      while msg:
        self.recv_events.put(parse_msg(msg))
        msg = self.pop_from_buffer()

  def pop_from_buffer(self):
    """parses a message read from the buffer"""
    # do we even know the length of the next message?
    if len(self.read_buffer) < 4:
      return None

    # have we received the entire next message?
    msg_length = struct.unpack('>I', self.read_buffer[:4])[0]
    if len(self.read_buffer) < (4 + msg_length):
      return None

    # okay, we have a complete message! lets return it!
    msg_ends_at = 4 + msg_length
    msg = self.read_buffer[4:msg_ends_at]
    self.read_buffer = self.read_buffer[msg_ends_at:]

    return json.loads(msg)

  def encode(self, msg):
    """encodes a message to send to the server"""
    jstr = json.dumps(msg)
    return struct.pack('>I%ds' % len(jstr), len(jstr), jstr)
