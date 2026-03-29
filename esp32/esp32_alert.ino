#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Invisible.";
const char* password = "12345678";
const char* serverUrl = "http://172.20.10.2:5001/api/alert-status";

const int ledPin = 2;
String currentState = "idle";

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
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
        currentState = "incoming";
      } else if (payload.indexOf("confirmed") >= 0) {
        currentState = "confirmed";
      } else {
        currentState = "idle";
      }
    }

    http.end();
  }

  if (currentState == "idle") {
    digitalWrite(ledPin, HIGH);
    delay(1000);
  }
  else if (currentState == "incoming") {
    digitalWrite(ledPin, HIGH);
    delay(200);
    digitalWrite(ledPin, LOW);
    delay(200);
  }
  else if (currentState == "confirmed") {
    digitalWrite(ledPin, HIGH);
    delay(800);
    digitalWrite(ledPin, LOW);
    delay(800);
  }
}