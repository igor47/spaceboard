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

static const uint32_t StateSendMS = 500; // ms
static const uint32_t BaudRate = 57600;  // baud

/*************** Data Types  *********************/
struct SerialCommand {
  enum Type {
    BAD = -1,
    NONE = 0,
    GETSTATE = 1,
    SETLED = 2,
    CLEARLEDS = 3,
  };
  SerialCommand() : type(BAD), ledNum(0), red(0), green(0), blue(0) { }
  SerialCommand(Type t) : type(t), ledNum(0), red(0), green(0), blue(0) { }

  Type type;
  uint8_t ledNum;
  uint8_t red;
  uint8_t green;
  uint8_t blue;
};

static struct State {
  State() : badCommandsReceived(0),
    commandsReceived(0),
    lastCommandTimestamp(0),
    lastStateSentTimestamp(0),
    runLED(false) { }
  unsigned long badCommandsReceived;
  unsigned long commandsReceived;
  unsigned long lastCommandTimestamp;
  unsigned long lastStateSentTimestamp;
  bool runLED;
} state;

/*************** Prototypes  *********************/

void send_state(unsigned long now);
SerialCommand read_server_command();
SerialCommand parse_command_buffer(const char* buf, int len);
void execute_command(const SerialCommand& cmd);
void toggle_led();
const char* scan_int(const char* buf, int* value);

/*************** CODE!!!!!!  *********************/

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // initialize serial
  Serial3.begin(BaudRate);

  // initialize leds
  strip.begin();
  strip.show();
}

void loop()
{
  // get the current time
  unsigned long now = millis();

  // if time overflows, reset last command timestamp to now instead of
  // having a ridiculous overflow. this happens every 50 days...
  if (state.lastCommandTimestamp > now)
    state.lastCommandTimestamp = now;

  // communicate with the server
  send_state(now);
  SerialCommand cmd = read_server_command();

  if (cmd.type == SerialCommand::NONE ||
      cmd.type == SerialCommand::BAD) {
    // log receiving bad commands
    if (cmd.type == SerialCommand::BAD) {
      state.badCommandsReceived++;
    }

  // got a good command from the server; log and execute
  } else {
    state.lastCommandTimestamp = now;
    state.commandsReceived++;
    execute_command(cmd);
  }
}

// sends the current program state to the computer
void send_state(unsigned long now)
{
  if (state.lastStateSentTimestamp != 0 &&
      now - state.lastStateSentTimestamp < StateSendMS) {
    return;
  }

  Serial3.print("C:");
  Serial3.print(state.commandsReceived, DEC);
  Serial3.print(";");

  Serial3.print("B:");
  Serial3.print(state.badCommandsReceived, DEC);
  Serial3.print(";");

  Serial3.print("L:");
  Serial3.print(now - state.lastCommandTimestamp, DEC);
  Serial3.print(";");

  Serial3.print("\r\n");

  state.lastStateSentTimestamp = now;
  toggle_led();
}

// reads data from the serial port and returns the last sent SerialCommand
SerialCommand read_server_command()
{
  // Commands end with a '\n'
  static char buf[20];
  static int buf_pos = 0;
  static bool buffer_overflow = false;
  char c;

  // read data from serial port and write it into buf
  while ((c = Serial.read()) != -1) {
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
  // S\n                -- causes an immediate send of the current state
  // L<char led>,<long c>\n -- sets the given led to the given color
  // X\n                -- clear (resets all of the leds)

  SerialCommand cmd;
  switch (buf[0]) {
  case 'S':
    cmd.type = SerialCommand::GETSTATE;
    break;
  case 'X':
    cmd.type = SerialCommand::CLEARLEDS;
    break;
  case 'L':
    cmd.type = SerialCommand::SETLED;
    int tmpN;
    buf = scan_int(buf+1, &tmpN);
    if (*buf != ',' || tmpN > UCHAR_MAX) {
      cmd.type = SerialCommand::BAD;
    } else {
      cmd.ledNum = tmpN;

      buf = scan_int(buf+1, &tmpN);
      if (*buf != '\n') {
        cmd.type = SerialCommand::BAD;
      } else {
        cmd.blue  = (tmpN >> 0) & 255;
        cmd.green = (tmpN >> 8) & 255;
        cmd.red   = (tmpN >> 16) & 255;
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
  if (cmd.type == SerialCommand::GETSTATE) {
    state.lastStateSentTimestamp = 0;
  }

  // set a particular led to a given color
  if (cmd.type == SerialCommand::SETLED) {
    strip.setPixelColor(cmd.ledNum, cmd.red, cmd.green, cmd.blue);
    strip.show();
  }

  // clear all the leds
  if (cmd.type == SerialCommand::CLEARLEDS) {
    for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, 0, 0, 0);
    }
    strip.show();
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
const char* scan_int(const char* buf, int *value)
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
