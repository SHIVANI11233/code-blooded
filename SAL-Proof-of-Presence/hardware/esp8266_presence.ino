/*
 * SAL - Proof-of-Presence: ESP8266 Presence Beacon
 * Broadcasts session signal. Only devices in the venue can receive it.
 * Hardware: ESP8266 (NodeMCU, Wemos D1 Mini)
 */

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* AP_SSID = "SAL_AI_WORKSHOP";
const char* AP_PASS = "sal2026";
const int CHANNEL = 6;
const char* SESSION_ID = "AI_WORKSHOP_R101";
const char* ROOM_ID = "R101";

ESP8266WebServer server(80);

void setup() {
  Serial.begin(115200);
  delay(100);

  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASS, CHANNEL);
  Serial.print("AP IP: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleSession);
  server.on("/session", handleSession);
  server.begin();
  Serial.println("SAL beacon ready. GET /session");
}

void loop() {
  server.handleClient();
}

void handleSession() {
  String nonce = String(random(0x7FFFFFFF), HEX);
  String json = "{";
  json += "\"session_id\":\"" + String(SESSION_ID) + "\",";
  json += "\"room_id\":\"" + String(ROOM_ID) + "\",";
  json += "\"timestamp\":\"2026-02-07T10:00:00Z\",";
  json += "\"nonce\":\"" + nonce + "\"";
  json += "}";

  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", json);
}
