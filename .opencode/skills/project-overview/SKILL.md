---
name: project-overview
description: Use when the user asks about the project structure, architecture, or how components connect. Trigger on "project overview", "architecture", "how it works", "structure", "diagram", "flow", "kien truc", "cau truc". Provides full project context for DATN IoT Security thesis.
---

# DATN IoT Security - Project Overview

## Project Name
**Xay dung giai phap truyen tin bao mat giua cac thiet bi IoT**

## Architecture

```
Xi (ESP32 + sensors + LoRa) --> LoRa --> Y Gateway (ESP32 + LoRa + WiFi)
                                               |
                                               v
                                    Flask Server (Python + SQLite)
                                               |
                                               v
                                    Dashboard (Web Map + Charts)
```

## Components

| Component | Location | Description |
|-----------|----------|-------------|
| Server | `server/app.py` | Flask API, AES decrypt, replay check |
| Dashboard | `server/dashboard.py` | Streamlit web map |
| Xi Node | `hardware/xi_node/` | ESP32 firmware |
| Y Gateway | `hardware/y_gateway/` | Gateway firmware |
| Wokwi | `wokwi/` | ESP32 simulation |
| Database | `iot_security.db` | SQLite with devices, telemetry |

## Device IDs

- `Xi_01` - ESP32 sensor node 1
- `Xi_02` - ESP32 sensor node 2
- `Y_01` - Gateway node

## Sensor Fields (JSON)

```json
{
  "id": "Xi_01",
  "t": 28.5,
  "h": 65.2,
  "p": 1008.0,
  "co2": 420,
  "co": 5.1,
  "nh3": 2.3,
  "lat": 21.00355,
  "lon": 105.84255,
  "alt": 10.0,
  "sats": 7,
  "gw": "Y_01",
  "seq": 1001
}
```

## API Endpoint

- `POST /receive-data` - Receive encrypted payload
- `GET /benchmark` - Get benchmark results

## Run Commands

```cmd
# Server
python server/app.py

# Dashboard
streamlit run server/dashboard.py

# Test
python server/main_test.py
```