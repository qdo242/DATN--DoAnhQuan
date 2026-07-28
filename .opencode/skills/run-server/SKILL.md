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

Server runs at `http://127.0.0.1:5000`

## Server Configuration

| Setting | Value |
|---------|-------|
| Host | 0.0.0.0 |
| Port | 5000 |
| AES Key | key_x_1234567890 |
| DB Path | ../iot_security.db |

## API Endpoints

### POST /receive-data
Receive encrypted payload from Wokwi/ESP32.

**Request**:
```json
{"payload": "hex_string"}
```

**Response**:
```json
{"status": "success", "device": "Xi_01"}
```

### GET /benchmark
Get benchmark results.

## Run Steps

1. Clone repository
2. `pip install -r requirements.txt`
3. `python server/init_db.py`
4. `python server/app.py`

## Test Server

```cmd
python server/main_test.py
```

## View Logs

```cmd
type server_debug.log
```