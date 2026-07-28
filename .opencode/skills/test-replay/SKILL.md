---
name: test-replay
description: Use when the user wants to test replay attack protection. Trigger on "test replay", "replay attack", "seq number", "sequence check", "anti-replay", "test bao mat", "kiem tra replay". Tests that old messages are rejected.
---

# Test Replay Attack Protection

## Quick Start

```cmd
cd C:\ĐATN\server
python test_replay.py
```

## Test Scripts

### 1. Basic Replay Test (7 cases)

```cmd
cd C:\ĐATN\server
python test_replay.py
```

**Test Cases**:
1. Normal message (seq=1001) → 200 OK
2. Duplicate (seq=1001) → 403 REPLAY
3. Older (seq=1000) → 403 REPLAY
4. New valid (seq=1002) → 200 OK
5. Out of order (seq=999) → 403 REPLAY
6. Same again (seq=1002) → 403 REPLAY
7. New valid (seq=1003) → 200 OK

### 2. Scenario Test (Advisor's requirement)

```cmd
cd C:\ĐATN\server
python test_replay_scenario.py
```

**Test Scenario (Hình 4.16)**:
1. Send seq=1001 → Server accepts (HTTP 200)
2. Resend same seq=1001 → Server rejects (HTTP 403)

## How Sequence Numbers Work

```
Client (ESP32)              Server
    |                         |
    |--- seq=1001 ----------->|  (OK, stored last_seq=1001)
    |<-- 200 OK --------------|
    |                         |
    |--- seq=1001 ----------->|  (REPLAY! 1001 <= 1001)
    |<-- 403 FORBIDDEN -------|
    |                         |
    |--- seq=1002 ----------->|  (OK, stored last_seq=1002)
    |<-- 200 OK --------------|
```

## Server Code (app.py)

```python
# Store last sequence per device
last_seq = {}

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.data.decode()
    device_id = decrypt_and_get_device_id(data)
    seq = get_seq_from_payload(data)
    
    # Check replay
    if seq <= last_seq.get(device_id, 0):
        logging.warning(f"REPLAY: device={device_id} seq={seq}")
        return jsonify({"error": "REPLAY"}), 403
    
    # Update last sequence
    last_seq[device_id] = seq
    
    # Process data...
    return jsonify({"status": "OK", "seq": seq})
```

## View Replay Logs

```cmd
findstr REPLAY server_debug.log
```

**Expected Output**:
```
REPLAY: device=Xi_01 seq=1001 (blocked)
REPLAY: device=Xi_01 seq=1000 (blocked)
```

## Test Output

```
=== REPLAY ATTACK TEST ===

Test 1: Send seq=1001
Result: 200 OK (expected: 200) ✓

Test 2: Resend seq=1001
Result: 403 REPLAY (expected: 403) ✓

Test 3: Send seq=1000 (older)
Result: 403 REPLAY (expected: 403) ✓

Test 4: Send seq=1002 (newer)
Result: 200 OK (expected: 200) ✓

Test 5: Send seq=999 (out of order)
Result: 403 REPLAY (expected: 403) ✓

Test 6: Resend seq=1002
Result: 403 REPLAY (expected: 403) ✓

Test 7: Send seq=1003 (newer)
Result: 200 OK (expected: 200) ✓

=== ALL TESTS PASSED ===
```

## Manual Testing

### Using curl
```cmd
# Send valid message
curl -X POST http://localhost:5000/ingest -d "encrypted_data"

# Resend same message (should fail)
curl -X POST http://localhost:5000/ingest -d "encrypted_data"
```

### Using Python requests
```python
import requests

# Send valid message
r = requests.post('http://localhost:5000/ingest', data=encrypted_data)
print(r.status_code)  # 200

# Resend same message
r = requests.post('http://localhost:5000/ingest', data=encrypted_data)
print(r.status_code)  # 403
```

## Common Issues

### Test Fails
1. Ensure server is running
2. Check AES key matches
3. Verify payload format

### Server Not Rejecting
1. Check `last_seq` dictionary is populated
2. Verify sequence number extraction
3. Check logging output

### All Tests Pass
- Replay protection is working correctly
- Server properly tracks sequence numbers
- Duplicate messages are rejected

## Related Files

| File | Purpose |
|------|---------|
| `test_replay.py` | Basic replay test (7 cases) |
| `test_replay_scenario.py` | Advisor's scenario test |
| `server/app.py` | Server with replay check |
| `server_debug.log` | Server logs with REPLAY entries |