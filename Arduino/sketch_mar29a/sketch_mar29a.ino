#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Invisible.";
const char* password = "12345678";
const char* serverUrl = "http://172.20.10.2:5001/api/alert-status";

const int ledPin = 2;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);

    int httpCode = http.GET();

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println(payload);

      if (payload.indexOf("incoming") >= 0) {
        // FAST BLINK
        digitalWrite(ledPin, HIGH);
        delay(100);
        digitalWrite(ledPin, LOW);
        delay(100);
      }
      else if (payload.indexOf("confirmed") >= 0) {
        // SOLID ON
        digitalWrite(ledPin, HIGH);
      }
      else {
        // OFF
        digitalWrite(ledPin, LOW);
      }
    }

    http.end();
  }

  delay(1000);
}