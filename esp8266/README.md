# ESP8266 Beacon for SAL Proof-of-Presence

Broadcasts a time-bound session signal. Only devices inside the venue (connected to this AP) can receive the session ID.

## Hardware

- ESP8266 (NodeMCU, Wemos D1 Mini, or similar)
- USB cable for flashing

## Setup

1. Install [Arduino IDE](https://www.arduino.cc/en/software)
2. Add ESP8266 board support: **File → Preferences → Additional Boards Manager URLs**
   ```
   http://arduino.esp8266.com/stable/package_esp8266com_index.json
   ```
3. **Tools → Board → Boards Manager** → search "esp8266" → Install
4. Select your board (e.g. **NodeMCU 1.0**)
5. Select the correct **Port**

## Flash

1. Open `sal_esp8266.ino` in Arduino IDE
2. Edit `AP_SSID`, `AP_PASS`, `SESSION_ID` if needed
3. Click **Upload**

## Usage

- ESP creates WiFi AP: `SAL_AI_WORKSHOP` / `sal2026`
- Connect your phone to this network
- App fetches `http://192.168.4.1/session` to get `session_id`
- Session ID proves physical presence (signal only in room)
