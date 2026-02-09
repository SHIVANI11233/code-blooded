#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// 🔐 WiFi credentials
const char* ssid = "iPhone";
const char* password = "123456789";

// 🌐 Backend server (your PC IP)
const char* serverUrl = "http://172.20.10.3:5000/presence";

// 📍 Fixed identifiers (can change later)
const char* USER_ID = "student_1";
const char* ROOM_ID = "ROOM101";
const char* SESSION_ID = "AI_WORKSHOP";

void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);

  // Wait for WiFi connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
  Serial.print("ESP8266 IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;
    WiFiClient client;

  
    String token = String(ROOM_ID) + "_" + String(SESSION_ID) + "_" + String(millis());

   
    String payload =
      "{\"user\":\"" + String(USER_ID) + "\",\"token\":\"" + token + "\"}";

    // 🔗 Send POST request
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(payload);

    Serial.println("-----");
    Serial.println("Sent Token:");
    Serial.println(token);
    Serial.print("HTTP Response Code: ");
    Serial.println(httpCode);

    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("Server Response:");
      Serial.println(response);
    } else {
      Serial.println("Error sending request");
    }

    http.end();
  } else {
    Serial.println("WiFi disconnected");
  }

  // ⏳ Send every 10 seconds
  delay(10000);
}
