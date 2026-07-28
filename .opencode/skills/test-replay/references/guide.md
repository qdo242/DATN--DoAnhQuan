# Replay Attack Test Guide

## How Sequence Numbers Work

1. Each device has a last-seen sequence number
2. New message must have seq > last seen
3. If seq <= last seen, reject with 403

## Test Cases

### test_replay.py (7 cases)

1. Normal message (seq=1001) → 200 OK
2. Duplicate (seq=1001) → 403 REPLAY
3. Older (seq=1000) → 403 REPLAY
4. New valid (seq=1002) → 200 OK
5. Out of order (seq=999) → 403 REPLAY
6. Same again (seq=1002) → 403 REPLAY
7. New valid (seq=1003) → 200 OK

### test_replay_scenario.py (Advisor's)

- Send seq=1001 → 200 OK
- Resend seq=1001 → 403 REPLAY

## Server Code (app.py)

```python
if seq <= last_seq.get(device_id, 0):
    logging.warning(f"REPLAY: device={device_id} seq={seq}")
    return jsonify({"error": "REPLAY"}), 403
last_seq[device_id] = seq
```