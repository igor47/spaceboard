/**
 * Blink
 *
 * Turns on an LED on for one second,
 * then off for one second, repeatedly.
 */
#include "Arduino.h"
#include "limits.h"

#include "Adafruit_NeoPixel.h"
#include "PacketSerial.h"

/*************** Data Types  *********************/
static struct State {
  State() : badCommandsReceived(0),
    commandsReceived(0),
    runLED(false) { }
  uint32_t badCommandsReceived;
  uint32_t commandsReceived;
  bool runLED;
} state;

/*************** Prototypes  *********************/

void send_state();
void toggle_led();
void onPacket(const uint8_t* buffer, size_t size);
void colorWipe(uint32_t c, uint8_t wait);
void clearStrip();

void arraySend(uint8_t byte);
void arrayLatch();
void arrayWipe();

void pwmSweep(uint8_t pin);

/*************** Constants *********************/

#undef LED_BUILTIN
#define LED_BUILTIN 33

#define LED_STRIP_PIN 14  // we chose a pin on GPIO port C in case we switch to DMA
#define LED_COUNT 60
Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_COUNT, LED_STRIP_PIN, NEO_GRB + NEO_KHZ800);

// the bit-shifted led array (not multi-color leds)
#define ARRAY_DATA_PIN  28
#define ARRAY_CLOCK_PIN 30
#define ARRAY_LATCH_PIN 31
#define ARRAY_COUNT 80

#define THROTTLE_SENSE_PIN 11
#define OXYGEN_PIN 10
#define SIGNAL_PIN 9

static const uint32_t BaudRate = 115200;  // baud
static PacketSerial packetSerial;


/*************** CODE!!!!!!  *********************/

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // initialize serial
  Serial3.begin(BaudRate);
  packetSerial.setPacketHandler(&onPacket);
  packetSerial.begin(&Serial3);
 
  // initialize leds
  strip.begin();
  strip.show();

  // NOTE: this causes some sort of initialization without which the led strip
  // doesn't work at all >:-|
  delay(1);
  // NOTE: DO NOT REMOVE ABOVE LINE

  // allows a quick visual check that all the leds work/a reset just happened
  colorWipe(strip.Color(20, 20, 20), 50);
  clearStrip();

  // initialize led array
  pinMode(ARRAY_LATCH_PIN, OUTPUT);
  digitalWrite(ARRAY_LATCH_PIN, LOW);  // latch should remain low unless we're loading
  pinMode(ARRAY_CLOCK_PIN, OUTPUT);
  digitalWrite(ARRAY_CLOCK_PIN, LOW);  // clock default to low
  pinMode(ARRAY_DATA_PIN, OUTPUT);
  digitalWrite(ARRAY_DATA_PIN, LOW);   // leave data pin low as well

  arrayWipe();

  // initialize analog input
  pinMode(THROTTLE_SENSE_PIN, INPUT_ANALOG);

  // test the analog meters
  pinMode(OXYGEN_PIN, PWM);
  pwmSweep(OXYGEN_PIN);

  pinMode(SIGNAL_PIN, PWM);
  pwmSweep(SIGNAL_PIN);

  // done!
  Serial.print("boot!\n");
}

void loop()
{
  // communicate with the server
  packetSerial.update();
}

void onPacket(const uint8_t* buffer, size_t size)
{
  toggle_led();

  if (size < 1) {
    state.badCommandsReceived++;
    return;
  }

  // Protocol from the server:
  uint32_t prevBad = state.badCommandsReceived;

  switch(buffer[0]) {
    // GET_STATE: causes an immediate send of the current state
    case 'G':
      send_state();
      break;
    // LATCH: forces a display of the led strip
    case 'L':
      strip.show();
      break;
    // CLEAR: resets all of the leds
    case 'C':
      clearStrip();
      break;

    // ONE_LED<led>,<r>,<g>,<b>: sets the given led to the given color
    case 'O':
      if(size == 5) {
        strip.setPixelColor(buffer[1], buffer[2], buffer[3], buffer[4]);
        break;
      } else {
        state.badCommandsReceived++;
      }
      break;

    // BATCH<first_led>,<r1>,<g1><b1>...<rN>,<gN>,<bN>: sets a bunch of entries at once
    case 'B':
      if(size >= 5 && (size - 2) % 3 == 0) {
        uint16_t pixel = (uint16_t)buffer[1];
        for(uint8_t cur = 2; cur < size; cur += 3) {
          strip.setPixelColor(pixel, buffer[cur], buffer[cur+1], buffer[cur+2]);
          pixel++;
        }
      } else {
        state.badCommandsReceived++;
      }
      break;

    // ARRAY<byte1>,<byte2>,...,<byteN> sets the array to given data
    case 'A':
      if(size == 1 + (ARRAY_COUNT / 8)) {
        for (unsigned int i = 1; i < size; i++) {
          arraySend(buffer[i]);
        }
        arrayLatch();
      } else {
        state.badCommandsReceived++;
      }
      break;

    // OXYGEN<byte> sets the oxygen meter to the specified place
    case 'X':
      if(size == 2) {
        unsigned int val = buffer[1];
        pwmWrite(OXYGEN_PIN, map(val, 0, 100, 0, 65535));
      } else {
        state.badCommandsReceived++;
      }
      break;

    // RESET: resets the device
    case 'R':
      nvic_sys_reset();
      break;  // we never get here

    // some unrecognized command is counted as bad
    default:
      state.badCommandsReceived++;
      break;
  }

  if (state.badCommandsReceived == prevBad) {
    state.commandsReceived += 1;
  }
}

// sends the current program state to the computer
void send_state()
{
  uint8_t packet[] = {
    'S', 
    (uint8_t)(state.commandsReceived >> 24),
    (uint8_t)(state.commandsReceived >> 16),
    (uint8_t)(state.commandsReceived >> 8),
    (uint8_t)(state.commandsReceived >> 0),

    (uint8_t)(state.badCommandsReceived >> 24),
    (uint8_t)(state.badCommandsReceived >> 16),
    (uint8_t)(state.badCommandsReceived >> 8),
    (uint8_t)(state.badCommandsReceived >> 0),
  };
  packetSerial.send(packet, 9);

  // also send over serial link
  Serial.print("C:");
  Serial.print(state.commandsReceived, DEC);
  Serial.print(";");

  Serial.print("B:");
  Serial.print(state.badCommandsReceived, DEC);
  Serial.print(";");

  Serial.print("\r\n");
}

void toggle_led()
{
  if(state.runLED) {
    digitalWrite(LED_BUILTIN, LOW);
    state.runLED = false;
  } else {
    digitalWrite(LED_BUILTIN, HIGH);
    state.runLED = true;
  }
}

static const uint32_t Blank = strip.Color(0, 0, 0);
void clearStrip() {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Blank);
  }
  strip.show();
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
      delay(wait);
  }
}

void arraySend(uint8_t byte) {
  uint8_t bit;

  for(uint8_t idx = 0; idx < 8; idx++) {
    bit = (byte >> idx) & 1;

    // put the data on the wire
    digitalWrite(ARRAY_DATA_PIN, bit);

    // clock the data into the shift register
    digitalWrite(ARRAY_CLOCK_PIN, HIGH);
    digitalWrite(ARRAY_CLOCK_PIN, LOW);
  }
}

void arrayLatch() {
  digitalWrite(ARRAY_LATCH_PIN, HIGH);
  digitalWrite(ARRAY_LATCH_PIN, LOW);
}

void arrayWipe() {
  uint8_t bit;

  toggle_led();

  // set pass-through mode for the latch
  digitalWrite(ARRAY_LATCH_PIN, HIGH);

  // set all the lights to on, one at a time
  digitalWrite(ARRAY_DATA_PIN, HIGH);
  for(bit = 0; bit < ARRAY_COUNT; bit++) {
    digitalWrite(ARRAY_CLOCK_PIN, HIGH);
    digitalWrite(ARRAY_CLOCK_PIN, LOW);
    delay(20);
  }

  // pause with all leds turned on
  toggle_led();
  delay(1000);

  // now set them all to off
  digitalWrite(ARRAY_DATA_PIN, LOW);
  for(bit = 0; bit < ARRAY_COUNT; bit++) {
    digitalWrite(ARRAY_CLOCK_PIN, HIGH);
    digitalWrite(ARRAY_CLOCK_PIN, LOW);
    delay(20);
  }

  // turn off pass-through
  digitalWrite(ARRAY_LATCH_PIN, LOW);
}

void pwmSweep(uint8_t pin) {
  for(int duty = 0; duty < 100; duty++) {
    pwmWrite(pin, map(duty, 0, 100, 0, 65535));
    delay(10);
  }

  pwmWrite(pin, 0);
}
