---
name: troubleshoot
description: Use when the user encounters errors or issues with the project. Trigger on "error", "bug", "fix", "loi", "khong chay duoc", "failed", "exception", "sua loi", "giup do". Helps diagnose and fix common problems.
---

# Troubleshooting Guide

## Common Errors

### 1. ModuleNotFoundError

**Error**:
```
ModuleNotFoundError: No module named 'flask'
```

**Solution**:
```cmd
pip install flask pycryptodomex requests
```

### 2. Port 5000 Already in Use

**Error**:
```
OSError: [WinError 10048] Only one usage of each socket address is permitted
```

**Solution**:
```cmd
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### 3. Database Locked

**Error**:
```
sqlite3.OperationalError: database is locked
```

**Solution**:
```cmd
del C:\ĐATN\iot_security.db
cd C:\ĐATN\server
python init_db.py
```

### 4. AES Decrypt Fails

**Error**:
```
ValueError: Incorrect AES key length
```

**Solution**:
- Check key: `key_x_1234567890` (16 bytes)
- Ensure IV is 16 bytes
- Verify payload is hex string

### 5. Wokwi Not Connecting

**Error**:
```
HTTPClient: Connection failed
```

**Solution**:
- Ensure server running on port 5000
- Check WiFi settings in diagram.json
- Verify URL in ESP32 code

### 6. Git Push Rejected

**Error**:
```
! [rejected] main -> main (non-fast-forward)
```

**Solution**:
```cmd
git pull origin main --allow-unrelated-histories
git push origin main
```

## Debug Commands

### Check Python Version
```cmd
python --version
```

### Check Installed Packages
```cmd
pip list
```

### View Server Logs
```cmd
type server_debug.log
```

### Test Server Health
```cmd
curl http://localhost:5000/health
```

### Check Port Usage
```cmd
netstat -ano | findstr :5000
```

### Check Database
```cmd
sqlite3 iot_security.db ".tables"
sqlite3 iot_security.db "SELECT * FROM devices;"
```

## Common Scenarios

### Server Won't Start
1. Check Python version
2. Check dependencies installed
3. Check port not in use
4. Check database exists

### Wokwi Not Sending Data
1. Ensure server running
2. Check WiFi connection
3. Verify URL is correct
4. Check firewall settings

### Benchmark Fails
1. Check database exists
2. Verify data in benchmark table
3. Check matplotlib installed

### Android Build Fails
1. Check Android Studio version
2. Sync Gradle
3. Check SDK path

## Get Help

1. Check `server_debug.log` for errors
2. Run `python init_db.py` to reset database
3. Verify all files in `server/` directory
4. Check GitHub issues

## Related Files

| File | Purpose |
|------|---------|
| `server_debug.log` | Server error logs |
| `server/init_db.py` | Database initialization |
| `requirements.txt` | Python dependencies |