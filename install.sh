#!/bin/bash

# fresh sources!
aptitude update

# we will need pip to install anything python-related
if [[ `which pip2` ]]
then
  echo "pip already installed";
else
  aptitude install -y python-pip
fi

# platformio is useful for anything arduino-related
if [[ `which platform` ]]
then
  echo "platformio already installed";
else
  pip install -U platformio
fi

# lets enable some hardware
. raspi-config nonint
if [ $(get_i2c) -eq 0 ]; then
  echo "i2c already enabled..."
else
  echo "enabling i2c..."
  do_i2c 0

  echo "installing i2c tools..."
  aptitude install -y i2c-tools python-smbus
  i2cdetect -y 1

  # https://github.com/fivdi/i2c-bus/blob/master/doc/raspberry-pi-i2c.md
  echo "setting i2c baudrate to 400mhz"
  if [[ $(grep 'i2c_arm_baudrate=400000' /boot/config.txt) ]]; then
    echo 'i2c frequency already set to 400kHz'
  else
    echo 'dtparam=i2c_arm_baudrate=400000' >> /boot/config.txt
    echo 'set frequency to 400kHz, but a reboot will be required'
  fi
fi

# do we have pigpio available?
if [[ `systemctl status pigpiod` ]]
then
  echo "pigpiod is already running..."
else
  aptitude install -y pigpio python-pigpio
  systemctl enable pigpiod
  systemctl start pigpiod
fi
