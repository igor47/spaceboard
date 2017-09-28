/**
 * Blink
 *
 * Turns on an LED on for one second,
 * then off for one second, repeatedly.
 */
#include "Arduino.h"

#undef LED_BUILTIN
#define LED_BUILTIN 33

/*************** Constants *********************/

const unsigned long StateSendMS = 100; // ms
const unsigned short BaudRate = 9600;  // baud

/*************** Data Types  *********************/

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
void toggle_led();

/*************** CODE!!!!!!  *********************/

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // initialize serial
  Serial3.begin(BaudRate);
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
