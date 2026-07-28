---
name: run-wokwi
description: Use when the user wants to run or debug the Wokwi ESP32 simulation. Trigger on "wokwi", "esp32", "run wokwi", "simulation", "sensor", "diagram.json", "chay wokwi", "mo phong". Wokwi simulates ESP32 sending encrypted sensor data.
---

# Run Wokwi Simulation

## Quick Start

1. Go to https://wokwi.com
2. Login with Google/GitHub
3. New Project → ESP32 DevKit V1
4. Copy 3 files from `wokwi/` folder:
   - `sketch.ino` → `sketch.ino`
   - `diagram.json` → `diagram.json`
   - `wokwi.toml` → `wokwi.toml`
5. Click "Start Simulation"

## Files

| File | Description |
|------|-------------|
| `wokwi/sketch.ino` | ESP32 firmware (WiFi + OLED + AES + HTTP) |
| `wokwi/diagram.json` | Circuit diagram (ESP32 + OLED SSD1306) |
| `wokwi/wokwi.toml` | Wokwi config |
| `wokwi/wokwi_to_copy.md` | Detailed copy-paste guide |
| `wokwi/libraries.txt` | Required libraries |

## Important

- Update `SERVER_URL` in `sketch.ino` to your localtunnel URL
- Device IDs are case-sensitive: `Xi_01` (not `XI_01`)
- Wokwi doesn't support BME280/LoRa/GPS - use random values

## Serial Monitor Output

```
WiFi connected
Beacon: B|Xi_01
ACK: A|Xi_01|Y_01
Sensor: t=28.5 h=62.3
Encrypted: a1b2c3...
HTTP 200 OK
```