#!/bin/bash

# should be run as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

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

# udev rules for platform
platformio_rules='/etc/udev/rules.d/99-platformio-udev.rules'
if [[ -e ${platformio_rules} ]]; then
  echo 'platformio udev rules already installed'
else
  wget https://raw.githubusercontent.com/platformio/platformio/develop/scripts/99-platformio-udev.rules -O ${platformio_rules}
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

# disable bluetooth
if [[ $(grep 'dtoverlay=pi3-disable-bt' /boot/config.txt) ]]; then
  echo 'bluetooth already disabled'
else
  echo 'dtoverlay=pi3-disable-bt' >> /boot/config.txt
  systemctl disable hciuart
  echo 'bluetooth disabled, but a reboot will be required'
fi

# disable serial console
# see: https://www.raspberrypi.org/documentation/configuration/uart.md
if [ $(get_serial) -eq 1 ]; then
  echo "serial already disabled"
else
  echo "disabling serial console"
  do_serial 1
  sed -i -e 's/enable_uart=./enable_uart=1/' /boot/config.txt
  echo "serial console disabled, but a reboot will be needed"
fi


# maple mini needs udev rules
maple_rules='/etc/udev/rules/d/45-maple.rules'
if [[ -e ${maple_rules} ]]; then
  echo 'maple mini udev rules already exist'
else
  wget https://raw.githubusercontent.com/rogerclarkmelbourne/Arduino_STM32/master/tools/linux64/45-maple.rules -O ${maple_rules}
fi
