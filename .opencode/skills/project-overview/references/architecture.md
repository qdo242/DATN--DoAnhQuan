# Project Architecture

## Component Diagram

```
+----------------+     +----------------+     +----------------+
|   Wokwi        |     |  Flask Server  |     |   SQLite DB    |
|   (ESP32)      |     |   (app.py)     |     | (iot_security) |
+----------------+     +----------------+     +----------------+
        |                      |                      |
        +----HTTP POST-------->+----INSERT------------>+
        |   (encrypted)        |   (decrypted)        |
        |                      |                      |
        +<---HTTP 200/403------+<---SELECT------------+
                               |   (seq check)        |
```

## Data Flow

1. ESP32 reads sensor data (temp, humidity, pressure, gas)
2. ESP32 creates JSON payload with sequence number
3. ESP32 encrypts payload with AES-128-CBC
4. ESP32 sends HTTP POST to server `/ingest`
5. Server decrypts payload
6. Server checks sequence number (anti-replay)
7. Server logs to database
8. Server returns 200 OK or 403 Forbidden

## Security Layers

- **Encryption**: AES-128-CBC with pre-shared key
- **Anti-replay**: Sequence number must be > last seen
- **Authentication**: Device ID in payload