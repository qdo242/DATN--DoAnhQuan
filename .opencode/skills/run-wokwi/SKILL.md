---
name: run-wokwi
description: Use when the user wants to run or debug the Wokwi ESP32 simulation. Trigger on "wokwi", "esp32", "run wokwi", "simulation", "sensor", "diagram.json", "chay wokwi", "mo phong". Wokwi simulates ESP32 sending encrypted sensor data.
---

# Run Wokwi Simulation

## Quick Start

1. Open VS Code with Wokwi extension
2. Open `wokwi/` folder
3. Click "Start Simulation" button
4. ESP32 connects to WiFi and sends data to server

## Files

| File | Purpose |
|------|---------|
| `wokwi/diagram.json` | Circuit diagram configuration |
| `wokwi/src/main.c` | ESP32 firmware (C code) |
| `wokwi/wokwi.toml` | Wokwi project config |

## Wokwi Extension

Install in VS Code:
```
Ext: Wokwi Simulator
ID: wokwi.wokwi-vscode
```

## Data Flow

```
ESP32 (Wokwi)
    ↓
Read Sensors (DHT22, BMP280, MQ-135)
    ↓
Create JSON Payload
    ↓
AES-128-CBC Encrypt
    ↓
HTTP POST to Server
    ↓
Server Decrypt + Validate
    ↓
Store in Database
```

## Sensor Fields (JSON)

```json
{
  "id": "Xi_01",
  "t": 28.5,
  "h": 62.3,
  "p": 1013.2,
  "co2": 420,
  "co": 3.5,
  "nh3": 2.1,
  "lat": 21.845,
  "lon": 104.098,
  "alt": 10.5,
  "sats": 8,
  "gw": "Y_01",
  "seq": 1001
}
```

| Field | Description | Unit | Range |
|-------|-------------|------|-------|
| id | Device ID | - | Xi_01, Xi_02 |
| t | Temperature | °C | 25-31 |
| h | Humidity | % | 58-65 |
| p | Pressure | hPa | 1005-1035 |
| co2 | CO2 | ppm | 380-450 |
| co | Carbon Monoxide | ppm | 2-8 |
| nh3 | Ammonia | ppm | 1-5 |
| lat | Latitude | degrees | 21.844-21.846 |
| lon | Longitude | degrees | 104.097-104.099 |
| alt | Altitude | meters | 8-15 |
| sats | GPS Satellites | count | 5-12 |
| gw | Gateway ID | - | Y_01 |
| seq | Sequence Number | integer | 1001+ |

## diagram.json Structure

```json
{
  "version": 1,
  "author": "Do Anh Quan",
  "editor": "wokwi",
  "parts": [
    {
      "type": "wokwi-esp32",
      "id": "esp",
      "top": 0,
      "left": 0
    },
    {
      "type": "wokwi-dht22",
      "id": "dht",
      "top": 0,
      "left": 200
    },
    {
      "type": "wokwi-bmp280",
      "id": "bmp",
      "top": 0,
      "left": 400
    }
  ],
  "connections": [
    ["esp:GND.1", "dht:GND", "black", []],
    ["esp:3V3", "dht:VCC", "red", []],
    ["esp:D4", "dht:SDA", "green", []]
  ]
}
```

## WiFi Configuration

```c
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASS ""
```

## Server URL

```c
#define SERVER_URL "http://10.0.2.2:5000/ingest"
```

**Note**: `10.0.2.2` is localhost from Wokwi emulator

## ESP32 Code Structure

```c
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Server URL
const char* serverUrl = "http://10.0.2.2:5000/ingest";

// Sequence number
int seq = 1001;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("WiFi connected");
}

void loop() {
  // Read sensors
  float t = readTemperature();
  float h = readHumidity();
  float p = readPressure();
  
  // Create JSON
  StaticJsonDocument<512> doc;
  doc["id"] = "Xi_01";
  doc["t"] = t;
  doc["h"] = h;
  doc["p"] = p;
  doc["seq"] = seq++;
  
  // Encrypt with AES
  String json = serializeJson(doc);
  String encrypted = aesEncrypt(json);
  
  // Send to server
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "text/plain");
  int httpResponseCode = http.POST(encrypted);
  
  if (httpResponseCode == 200) {
    Serial.println("Data sent OK");
  } else if (httpResponseCode == 403) {
    Serial.println("Replay detected!");
  }
  
  http.end();
  delay(5000);  // Send every 5 seconds
}
```

## Common Issues

### WiFi Not Connecting
- Check `WIFI_SSID` and `WIFI_PASS`
- Ensure internet connection
- Try `Wokwi-GUEST` (no password)

### Server Not Receiving
- Ensure server running on port 5000
- Check URL: `http://10.0.2.2:5000/ingest`
- Verify firewall settings

### AES Decrypt Fails
- Check key: `key_x_1234567890`
- Ensure IV is 16 bytes
- Verify payload is hex string

### Simulation Too Slow
- Reduce `delay()` in loop
- Check sensor read times
- Verify WiFi signal strength

## Debug Output

Wokwi Serial Monitor shows:
```
WiFi connected
Temperature: 28.5°C
Humidity: 62.3%
Pressure: 1013.2 hPa
Sending data...
Response: 200 OK
```

## Wokwi Tips

- Use Serial Monitor for debugging
- Check pin connections in diagram.json
- Verify sensor libraries are included
- Test with simple blink first