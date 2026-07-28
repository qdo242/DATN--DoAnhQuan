---
name: project-overview
description: Use when the user asks about the project structure, architecture, or how components connect. Trigger on "project overview", "architecture", "how it works", "structure", "diagram", "flow", "kien truc", "cau truc". Provides full project context for DATN IoT Security thesis.
---

# DATN IoT Security - Project Overview

## Project Name
**Xay dung giai phap truyen tin bao mat giua cac thiet bi IoT**

## Student
- Ho ten: Do Anh Quan
- GV huong dan: Thay Hai (Haihd)
- Co so: HUCE (Hoc vien Xay dung)

## Architecture

```
+------------------+     +------------------+     +------------------+
|   Wokwi (ESP32)  |     |  Flask Server    |     |   SQLite DB      |
|   Sensor Node    |     |   (app.py)       |     | (iot_security.db)|
+------------------+     +------------------+     +------------------+
         |                        |                        |
         +----HTTP POST---------->+----INSERT-------------->+
         |   (AES encrypted)      |   (decrypted JSON)     |
         |                        |                        |
         +<---HTTP 200/403--------+<---SELECT--------------+
         |   (response)           |   (seq check)          |
         |                        |                        |
         +                        +                        +
              WiFi/BLE                   TCP/IP                File-based
```

## Components

### 1. Wokwi (ESP32 Simulator)
- **Location**: `wokwi/`
- **Files**: `diagram.json`, `src/main.c`
- **Purpose**: Simulate ESP32 sending encrypted sensor data
- **Sensors**: Temperature, Humidity, Pressure, CO2, CO, NH3
- **GPS**: Latitude, Longitude, Altitude, Satellites
- **Crypto**: AES-128-CBC encryption

### 2. Flask Server
- **Location**: `server/`
- **Files**: `app.py`, `xor_cipher.py`, `benchmark_crypto.py`
- **Port**: 5000
- **Purpose**: Receive, decrypt, validate, and store IoT data
- **Features**: 
  - AES decryption
  - Anti-replay (sequence number check)
  - Benchmark logging

### 3. Android App
- **Location**: `android/`
- **Purpose**: Display real-time IoT data
- **Connection**: BLE to ESP32 gateway

### 4. Database
- **Location**: `iot_security.db`
- **Engine**: SQLite
- **Tables**: devices, telemetry, benchmark

## Key Files

| File | Purpose |
|------|---------|
| `server/app.py` | Flask API server (main) |
| `server/xor_cipher.py` | XOR encryption (reference only) |
| `server/benchmark_crypto.py` | AES vs XOR comparison |
| `server/test_replay.py` | Replay attack tests (7 cases) |
| `server/test_replay_scenario.py` | Advisor's scenario test |
| `server/init_db.py` | Database initialization |
| `doandocs/Chương 3.docx` | Security design chapter |
| `docs/images/` | Generated charts and diagrams |

## Crypto Details

### AES-128-CBC
- **Key**: `key_x_1234567890` (16 bytes)
- **Mode**: CBC (Cipher Block Chaining)
- **IV**: Random 16 bytes (prepended to ciphertext)
- **Padding**: Zero padding to 16-byte blocks
- **Usage**: Production encryption

### XOR Cipher
- **Key**: `ABC123` (6 bytes)
- **Mode**: Simple XOR
- **Usage**: Reference/benchmark only (NOT secure)

### Anti-Replay
- **Method**: Sequence number tracking
- **Rule**: New seq must be > last seen seq
- **Response**: HTTP 403 if replay detected

## Database Schema

```sql
-- Device registry
CREATE TABLE devices (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Telemetry logs
CREATE TABLE telemetry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id TEXT NOT NULL,
  encrypted_payload TEXT,
  decrypted_json TEXT,
  seq INTEGER,
  status TEXT,
  decrypt_ms REAL,
  seq_ms REAL,
  log_ms REAL,
  total_ms REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (device_id) REFERENCES devices(id)
);

-- Benchmark results
CREATE TABLE benchmark (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id TEXT NOT NULL,
  payload_size INTEGER,
  encrypt_ms REAL,
  decrypt_ms REAL,
  seq_ms REAL,
  log_ms REAL,
  total_ms REAL,
  status TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Device IDs

| ID | Name | Type | Description |
|----|------|------|-------------|
| Xi_01 | ESP32 Sensor 1 | sensor | Main sensor node |
| Xi_02 | ESP32 Sensor 2 | sensor | Secondary sensor node |
| Y_01 | Gateway | gateway | Data collection gateway |

## Sensor Fields (JSON Payload)

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

| Field | Description | Unit |
|-------|-------------|------|
| id | Device ID | - |
| t | Temperature | °C |
| h | Humidity | % |
| p | Pressure | hPa |
| co2 | CO2 | ppm |
| co | CO | ppm |
| nh3 | NH3 | ppm |
| lat | Latitude | decimal degrees |
| lon | Longitude | decimal degrees |
| alt | Altitude | meters |
| sats | Satellites | count |
| gw | Gateway ID | - |
| seq | Sequence number | integer |

## Performance Metrics

| Metric | Value |
|--------|-------|
| AES Decrypt | 0.049ms avg |
| Seq Check | 3.634ms avg |
| DB Write | 6.909ms avg |
| Total Request | 10.455ms avg |
| Success Rate | 78.9% (15/19) |
| Replay Blocked | 4 requests |

## Git Repository

- **URL**: https://github.com/qdo242/DATN--HUCE
- **Branch**: main
- **Remote**: origin