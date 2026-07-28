---
name: run-server
description: Use when the user wants to start, stop, or debug the Flask server. Trigger on "run server", "start server", "flask", "app.py", "server error", "port 5000", "api", "chay server", "khoi dong server". The server runs on port 5000 with AES decryption.
---

# Run Flask Server

## Quick Start

```cmd
cd C:\ĐATN\server
python app.py
```

Server runs at `http://localhost:5000`

## Server Configuration

| Setting | Value |
|---------|-------|
| Host | 0.0.0.0 |
| Port | 5000 |
| Debug | False (default) |
| AES Key | key_x_1234567890 |
| DB Path | ../iot_security.db |

## API Endpoints

### POST /ingest
Receive encrypted payload from Wokwi/ESP32.

**Request**: Encrypted hex string (IV + ciphertext)

**Response**:
```json
// Success (200)
{"status": "OK", "seq": 1001}

// Replay detected (403)
{"error": "REPLAY", "seq": 1001}

// Bad request (400)
{"error": "Invalid payload"}
```

### GET /devices
List all registered devices.

**Response**:
```json
[
  {"id": "Xi_01", "name": "ESP32 Sensor 1", "type": "sensor"},
  {"id": "Xi_02", "name": "ESP32 Sensor 2", "type": "sensor"},
  {"id": "Y_01", "name": "Gateway", "type": "gateway"}
]
```

### GET /telemetry
Get telemetry data logs.

**Query Parameters**:
- `limit` (int): Max records (default 100)
- `device` (string): Filter by device ID

**Response**:
```json
[
  {
    "id": 1,
    "device_id": "Xi_01",
    "status": "OK",
    "seq": 1001,
    "total_ms": 10.455
  }
]
```

### GET /benchmark
Get benchmark results.

**Response**:
```json
[
  {
    "id": 1,
    "device_id": "Xi_01",
    "decrypt_ms": 0.049,
    "total_ms": 10.455,
    "status": "OK"
  }
]
```

### GET /health
Health check endpoint.

**Response**:
```json
{"status": "healthy", "uptime": 3600}
```

## Dependencies

```cmd
pip install flask pycryptodomex requests
```

## Common Issues & Solutions

### Port 5000 Already in Use
```cmd
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### ModuleNotFoundError
```cmd
pip install flask pycryptodomex requests
```

### Database Error
```cmd
cd C:\ĐATN\server
python init_db.py
```

### AES Decrypt Fails
- Check key: `key_x_1234567890` (16 bytes)
- Ensure IV is 16 bytes
- Verify payload is hex string

### Server Won't Start
1. Check Python version: `python --version`
2. Check dependencies: `pip list`
3. Check port: `netstat -ano | findstr :5000`
4. Check logs: `type server_debug.log`

## Debug Mode

```cmd
cd C:\ĐATN\server
set FLASK_DEBUG=1
python app.py
```

## View Logs

```cmd
type server_debug.log
```

## Test Server

```cmd
curl http://localhost:5000/health
curl http://localhost:5000/devices
```

## Server Code Structure

```
server/
├── app.py                    # Main Flask application
├── xor_cipher.py             # XOR encryption (reference)
├── benchmark_crypto.py       # AES vs XOR benchmark
├── test_replay.py            # Replay attack tests
├── test_replay_scenario.py   # Advisor's scenario test
├── init_db.py                # Database initialization
└── server_debug.log          # Server logs
```

## API Usage Examples

### Using curl
```cmd
# Health check
curl http://localhost:5000/health

# Get devices
curl http://localhost:5000/devices

# Get telemetry
curl "http://localhost:5000/telemetry?limit=10"
```

### Using Python requests
```python
import requests

# Health check
r = requests.get('http://localhost:5000/health')
print(r.json())

# Get devices
r = requests.get('http://localhost:5000/devices')
print(r.json())
```