# Server API Reference

## Endpoints

### POST /ingest
Receive encrypted payload from ESP32.

**Request Body**: Encrypted hex string (16 byte IV + ciphertext)

**Response**:
- 200: `{"status": "OK", "seq": 1234}`
- 403: `{"error": "REPLAY", "seq": 1234}`

### GET /devices
List all registered devices.

**Response**: Array of device objects

### GET /telemetry
Get telemetry logs.

**Query Params**: `?limit=100&device=Xi_01`

### GET /benchmark
Get benchmark results.

### GET /health
Health check.

**Response**: `{"status": "healthy"}`

## Error Codes

- 400: Bad request (invalid payload)
- 403: Replay attack detected
- 500: Server error