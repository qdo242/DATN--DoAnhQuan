# Wokwi Configuration

## diagram.json Structure

```json
{
  "version": 1,
  "author": "Do Anh Quan",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-esp32", "id": "esp", "top": 0, "left": 0 },
    { "type": "wokwi-dht22", "id": "dht", "top": 0, "left": 200 }
  ],
  "connections": [
    ["esp:GND.1", "dht:GND", "black", []],
    ["esp:3V3", "dht:VCC", "red", []],
    ["esp:D4", "dht:SDA", "green", []]
  ]
}
```

## WiFi Config

```c
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASS ""
```

## Server URL

```c
#define SERVER_URL "http://10.0.2.2:5000/ingest"
```

Note: `10.0.2.2` is localhost from Wokwi emulator