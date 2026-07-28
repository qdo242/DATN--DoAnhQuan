# Database Schema

## Tables

### devices
```sql
CREATE TABLE devices (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### telemetry
```sql
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
```

### benchmark
```sql
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

## Sample Queries

```sql
-- Get all devices
SELECT * FROM devices;

-- Get recent telemetry
SELECT * FROM telemetry ORDER BY id DESC LIMIT 10;

-- Get benchmark stats
SELECT device_id, AVG(total_ms), COUNT(*) 
FROM benchmark GROUP BY device_id;
```