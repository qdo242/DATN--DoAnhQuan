---
name: db-query
description: Use when the user wants to query or inspect the SQLite database. Trigger on "database", "db query", "sqlite", "iot_security", "xem du lieu", "truy van", "kiem tra db". Database has 3 tables: devices, telemetry, benchmark.
---

# Query SQLite Database

## Database Location

`C:\ĐATN\iot_security.db`

## Tables

| Table | Records | Description |
|-------|---------|-------------|
| devices | 3 | Xi_01, Xi_02, Y_01 |
| telemetry | varies | Encrypted payload logs |
| benchmark | 19 | Performance test results |

## Real Data

### Devices (3 records)
| ID | Name | Type |
|----|------|------|
| Xi_01 | ESP32 Sensor 1 | sensor |
| Xi_02 | ESP32 Sensor 2 | sensor |
| Y_01 | Gateway | gateway |

### Benchmark (19 records)
- 15 OK (78.9%)
- 4 FAIL (21.1%) - replay blocked
- Avg Decrypt: 0.049ms
- Avg Total: 10.455ms

## Quick Commands

### List all devices
```cmd
cd C:\ĐATN
sqlite3 iot_security.db "SELECT * FROM devices;"
```

### View benchmark results
```cmd
sqlite3 iot_security.db "SELECT id, device_id, decrypt_ms, seq_ms, total_ms, status FROM benchmark ORDER BY id;"
```

### Count by status
```cmd
sqlite3 iot_security.db "SELECT status, COUNT(*) FROM benchmark GROUP BY status;"
```

### Average performance
```cmd
sqlite3 iot_security.db "SELECT device_id, AVG(total_ms), COUNT(*) FROM benchmark GROUP BY device_id;"
```

## Schema

### devices
```sql
CREATE TABLE devices (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

## Useful Queries

### Get all OK records
```cmd
sqlite3 iot_security.db "SELECT * FROM benchmark WHERE status='OK';"
```

### Get all FAIL records
```cmd
sqlite3 iot_security.db "SELECT * FROM benchmark WHERE status='FAIL';"
```

### Get performance by device
```cmd
sqlite3 iot_security.db "SELECT device_id, AVG(decrypt_ms), AVG(total_ms) FROM benchmark GROUP BY device_id;"
```

### Get recent 5 records
```cmd
sqlite3 iot_security.db "SELECT * FROM benchmark ORDER BY id DESC LIMIT 5;"
```

## Reset Database

```cmd
cd C:\ĐATN
del iot_security.db
cd server
python init_db.py
```

## Export to CSV

```cmd
sqlite3 -header -csv iot_security.db "SELECT * FROM benchmark;" > benchmark.csv
```