
# spaceboard #

the files for my spaceteam console.
this repo is a [platformio](http://platformio.org/) project and also a python project meant to run on a raspberry pi.

## microcontroller ##

the platformio files are in `src/` and `lib`, and control the on-board microcontroller.
i am using [this maple-mini clone](http://amzn.to/2k5Q6A4) which is 5x more expensive than a bluepill, but is available next-day on amazon and has nice buttons instead of jumpers and correct pull-up resistors/bootloader for usb programming.

the maple-mini can be programmed by running `platformio run --target upload`.
in some cases, the ACM device is not enabled or is stuck (like, if you accidentally wrote a busy-loop that spews to `Serial`).
you can get around this by booting the microcontroller into [perpetual bootloader mode](http://wiki.stm32duino.com/index.php?title=Perpetual_bootloader).
in that mode, the device will boot straight into DFU mode.
you'll need to add the DFU port to program it.
on the raspberry pi, it'll be something like `platformio run --target upload --upload-port <path-in-dev>`.
you can figure out what the path is by running `sudo strace -e open dfu-util -l`

## raspberry pi ##

i used [this pi that comes with a case and heatsinks](http://amzn.to/2xKNtbG) and [this breakout board/cable](http://amzn.to/2fFmc4l).
i had problems powering the pi with a random 5V power supply -- undervoltages would cause reboots.
using an [official power supply](http://amzn.to/2fDrOvQ) made life easier.

### python ###

to run the python controller, invoke `spaceteam.py`.
it doesn't need `root` atm.

### install.sh ###

the file `install.sh` will correctly configure the pi so that the python project works.
there are quite a few settings, especially those controlling the i2c device, disable bluetooth so that hardware serial is available, disable serial consoles, etc...
the script will also install various dependencies, including `platformio` and various python modules.

run it as root on your raspberry pi:

```bash
$ sudo ./install.sh
```

### peripherals ###

the `spaceteam` directory contains the python project files.
there are device drivers for several peripherals attached to the pi:

* microcontroller - controls comms with the microcontroller (maple mini)
* mcp23017 - this is digital IO multiplexer, we talk to it over i2c. i used [this one](https://www.adafruit.com/product/732) and have a few spares
* ads1115 - an ADC, also on the i2c bus. i used [this one off amazon (yay next-day delivery)](http://amzn.to/2x1RBk8)

## lights ##

for any on-board lights, i used a single WS2812 run.
ws2812 leds are often known as [neopixels](https://www.adafruit.com/category/168) in the hobbyist community.
i used [this generic one](http://amzn.to/2xKR61G) off amazon.

in hindsight, ws2812 is not a good choice for this project.
it's very difficult to drive off the raspberry pi.
i tried [this library](https://github.com/jgarff/rpi_ws281x) but the DMA was causing segfaults (with SPI) or DMA errors which put the filesystem into RO (with PCM).
in the end, it was easier to run the lights off a microcontroller where precise timing is easier.
even there people often use DMA, but i found a bit-banged library that seems to work pretty well without consuming an entire IO port.

_don't forget about level-shifting the lights!!!_
thankfully, there's an [easy, elegant hack that just involves one diode](https://hackaday.com/2017/01/20/cheating-at-5v-ws2812-control-to-use-a-3-3v-data-line/).

## serial io ##

to talk between the pi and the microcontroller, i used [a binary protocol](https://www.embeddedrelated.com/showarticle/113.php) over serial.
this is fast and efficient, i highly recommend using it.
the microcontroller library is in `lib/PacketSerial` and on the python side the code in `spaceteam/microcontroller.py` uses a [built-in library](https://pythonhosted.org/cobs/cobs.cobs.html#cobs-examples).
TODO: i haven't figured out how to *read* the data off the microcontroller from python yet, since python 2.7 removes the ability to set a custom `eol` character for `serial.readline()`; i'll probably have to read one char at a time, but still a binary protocol is way faster and more reliable.

## wiring overview ##

no diagram right now.
the basic idea is:

* raspberry pi is connected to an ethernet hub and to power supply via microusb port
* pi I2C bus is connected to an ads1115 and an mcp23017
* pi `/dev/serial0` tty is connected to `Serial3` on the maple mini
* pi USB connected to maple mini USB for programming (via `platformio`) and debugging (via `Serial` on maple and `miniterm.py` on Pi)
* maple mini is connected to led strip
* potentiometers on the ads1115, switches on the mcp23017
* 3.3V bus powers all the peripherals
* LED strip powered by separate 5V power brick

## switches ##

i used a bunch of buttons and switches off amazon:

* [light-up rockers](http://amzn.to/2xKVnSN)
* [big toggles](http://amzn.to/2xOSAbw)
* [small momentary push-buttons](http://amzn.to/2fBGNGL)
* [mid-size toggles](http://amzn.to/2xFJn2Y)
* [cheap 7-segment displays](http://amzn.to/2fD8jnq)
* [giant push-buttons](http://amzn.to/2fEda7D)
