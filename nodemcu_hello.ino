/*
  This programme waits for a JSON
  object with the key of "message"
  and value of "on" to then serial write
  a json object which is read by python
  to determine this device's path in the
  computer. Upon a successfuly sending
  and recieving message, the builtin LED
  turns on and off for the different
  devices

  @techscapades 2023 https://github.com/techscapades

*/

#include <ArduinoJson.h>
const int ledPin = LED_BUILTIN;
//this baud rate must be the same as with the python code
const int baud_rate = 115200;

void setup() {
  Serial.begin(baud_rate);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
}

void loop() {
  read_serial();
}

void read_serial() {
  /*
    This fucntion waits for the message
    to arrive from python
  */
  if (Serial.available()) {
    String jsonString = Serial.readStringUntil('\n');
    DynamicJsonDocument jsonDoc(64); // Adjust the size if needed
    DeserializationError error = deserializeJson(jsonDoc, jsonString);

    if (error) {
      Serial.print("JSON parsing error: ");
      Serial.println(error.c_str());
    } else {
      const char* message = jsonDoc["message"];
      if (message && strcmp(message, "on") == 0) {
        digitalWrite(ledPin, HIGH);
        write_serial();
      }
      digitalWrite(ledPin, HIGH);
    }
  }
}

void write_serial() {
  /*
    This function sends the response
    in JSON with keys of device
    and message. The value of message
    is a flag on the python side for
    programme control
  */
  StaticJsonDocument<64> jsonDoc;
  jsonDoc["message"] = "hello";
  jsonDoc["device"] = "nmcu_1";
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  Serial.println(jsonString);
  digitalWrite(ledPin, LOW);
  delay(1000);
}
