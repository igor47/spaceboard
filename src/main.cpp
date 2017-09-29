/**
 * Blink
 *
 * Turns on an LED on for one second,
 * then off for one second, repeatedly.
 */
#include "Arduino.h"
#include "limits.h"

#include "Adafruit_NeoPixel.h"

/*************** Constants *********************/

#undef LED_BUILTIN
#define LED_BUILTIN 33

#define LED_STRIP_PIN 14  // we chose a pin on GPIO port C in case we switch to DMA
Adafruit_NeoPixel strip = Adafruit_NeoPixel(20, LED_STRIP_PIN, NEO_GRB + NEO_KHZ800);

static const uint32_t BaudRate = 256000;  // baud
//static const uint32_t BaudRate = 9600;  // baud
static uint32_t loopTime = 0;

/*************** Data Types  *********************/
struct Color {
  Color() : red(0), green(0), blue(0) { }
  Color(uint8_t r, uint8_t g, uint8_t b) : red(r), green(g), blue(b) { }

  uint8_t red;
  uint8_t green;
  uint8_t blue;
};

struct SerialCommand {
  enum Type {
    BAD = -1,
    NONE = 0,
    GET_STATE = 1,
    CLEAR_LEDS = 2,
    ONE_LED = 3,
    BATCH_LEDS = 4,
    LATCH = 5,
  };
  SerialCommand() : type(BAD), ledNum(0), ledCount(0), color(0) { }
  SerialCommand(Type t) : type(t), ledNum(0), ledCount(0), color(0) { }

  Type type;
  uint16_t ledNum;
  uint16_t ledCount;
  Color *color;
};

static struct State {
  State() : badCommandsReceived(0),
    commandsReceived(0),
    runLED(false) { }
  unsigned long badCommandsReceived;
  unsigned long commandsReceived;
  bool runLED;
} state;

/*************** Prototypes  *********************/

void send_state();
SerialCommand read_server_command();
SerialCommand parse_command_buffer(const char* buf, int len);
void execute_command(const SerialCommand& cmd);
void toggle_led();
const char* scan_int(const char* buf, int* value);
void val_to_color(uint32_t val, Color *c);

/*************** CODE!!!!!!  *********************/

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // initialize serial
  Serial3.begin(BaudRate);
  Serial3.print("boot!\r\n");

  // initialize leds
  strip.begin();
  strip.show();
}

void loop()
{
  // get the current time
  loopTime = millis();

  // communicate with the server
  SerialCommand cmd = read_server_command();
  if (cmd.type == SerialCommand::NONE ) {
    // nothing to do
  } else if (cmd.type == SerialCommand::BAD) {
    // log receiving bad commands
    state.badCommandsReceived++;

  // got a good command from the server; log and execute
  } else {
    state.commandsReceived++;
    execute_command(cmd);
  }
}

// sends the current program state to the computer
void send_state()
{
  Serial3.print("C:");
  Serial3.print(state.commandsReceived, DEC);
  Serial3.print(";");

  Serial3.print("B:");
  Serial3.print(state.badCommandsReceived, DEC);
  Serial3.print(";");

  Serial3.print("\r\n");
  toggle_led();
}

// reads data from the serial port and returns the last sent SerialCommand
SerialCommand read_server_command()
{
  // Commands end with a '\n'
  static char buf[20];
  static int buf_pos = 0;
  static bool buffer_overflow = false;

  // read data from serial port and write it into buf
  char c;
  while (Serial3.available()) {
    c = Serial3.read();
    buf[buf_pos] = c;

    // we've read a whole command once we see a '\n'
    if (c == '\n') {
      break;

    } else {
      buf_pos++;

      if (buf_pos == sizeof(buf)) {
        buf_pos = 0;
        buffer_overflow = true;
        // we keep looping to consume the rest of the data in the buffer
      }
    }
  }

  // we read a full command from the serial port
  if (buf[buf_pos] == '\n') {
    SerialCommand cmd;
    if (buffer_overflow) {
      cmd = SerialCommand(SerialCommand::BAD);
    } else {
      cmd = parse_command_buffer(buf, buf_pos);
    }

    buf_pos = 0;
    buffer_overflow = false;
    for (unsigned int i = 0; i < sizeof(buf); i++) {
        buf[i] = 0;
    }

    return cmd;

  // haven't read a full command yet; lets return no command
  } else {
    return SerialCommand(SerialCommand::NONE);
  }
}

// parses string read from incoming serial from the computer into a SerialCommand
SerialCommand parse_command_buffer(const char* buf, int len)
{
  // Protocol from the server:
  // G\n                -- causes an immediate send of the current state
  // L\n                -- latch (forces a display of the led strip)
  // C\n                -- clear (resets all of the leds)
  // O<char led>,<long c>\n -- sets the given led to the given color
  // B<char start>,<char count>,[<long c>]\n -- updates a bunch of led colors

  // we declare this as an array to support the BATCH_LEDS command in the future
  // the ONE_LED command only uses the first element of this static array
  static Color c[10];

  SerialCommand cmd;
  switch (buf[0]) {
  case 'G':
    cmd.type = SerialCommand::GET_STATE;
    break;
  case 'L':
    cmd.type = SerialCommand::LATCH;
    break;
  case 'C':
    cmd.type = SerialCommand::CLEAR_LEDS;
    break;
  case 'O':
    cmd.type = SerialCommand::ONE_LED;
    cmd.ledCount = 1;

    int tmpN;

    // scan the integer identifying the led
    buf = scan_int(buf+1, &tmpN);
    if (*buf != ',' || tmpN > UCHAR_MAX) {
      cmd.type = SerialCommand::BAD;

    // scan the integer identifying the color
    } else {
      cmd.ledNum = (uint16_t)tmpN;

      buf = scan_int(buf+1, &tmpN);
      if (*buf != '\n' && *buf != '\r') {
        cmd.type = SerialCommand::BAD;
      } else {
        val_to_color(tmpN, &c[0]);
        cmd.color = &c[0];
      }
    }
    break;
  default:
    cmd.type = SerialCommand::BAD;
  }

  return cmd;
}

void execute_command(const SerialCommand& cmd)
{
  // send state now (well, next loop)
  if (cmd.type == SerialCommand::GET_STATE) {
    send_state();
  }

  // latch -- display the current state of the led array
  if (cmd.type == SerialCommand::LATCH) {
    strip.show();
  }

  // set a particular led to a given color
  if (cmd.type == SerialCommand::ONE_LED) {
    Color c = cmd.color[0];
    strip.setPixelColor(cmd.ledNum, c.red, c.green, c.blue);
  }

  // clear all the leds
  if (cmd.type == SerialCommand::CLEAR_LEDS) {
    for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, 0, 0, 0);
    }
    strip.show();
  }

  // set a group of LEDs
  if (cmd.type == SerialCommand::BATCH_LEDS) {
  }
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

// used to read an integer from serial data
const char* scan_int(const char* buf, int* value)
{
  // initialize the value
  *value = 0;

  // determine the sign of the value
  int sign = 1;
  if (buf[0] == '-') {
    sign = -1;
    buf++;
  }

  // parse the value -- works as long as we encounter valid numbers
  while (*buf >= '0' && *buf <= '9') {
    *value = (10 * (*value)) + (*buf - '0');
    buf++;
  }

  // we're done
  *value = *value * sign;
  return buf;
}

void val_to_color(uint32_t val, Color *c)
{
  c->blue  = (uint8_t)(val >> 0);
  c->green = (uint8_t)(val >> 8);
  c->red   = (uint8_t)(val >> 16);
}
