# Troubleshooting Reference

## Error Solutions

### Python Errors

| Error | Solution |
|-------|----------|
| ModuleNotFoundError | `pip install <package>` |
| SyntaxError | Check Python version (3.8+) |
| IndentationError | Check tabs/spaces |

### Server Errors

| Error | Solution |
|-------|----------|
| Port 5000 in use | `netstat -ano \| findstr :5000` then `taskkill /PID <id> /F` |
| Address already in use | Wait or change port |
| DB locked | Delete and reinit DB |

### Wokwi Errors

| Error | Solution |
|-------|----------|
| WiFi fail | Check SSID/password |
| Server unreachable | Ensure server running |
| AES decrypt fail | Check key matches |

### Git Errors

| Error | Solution |
|-------|----------|
| Push rejected | `git pull origin main --allow-unrelated-histories` |
| Merge conflict | Resolve manually |
| Permission denied | Check GitHub auth |

## Debug Commands

```cmd
# Check Python
python --version
pip list

# Check server
curl http://localhost:5000/health

# Check DB
sqlite3 iot_security.db ".tables"

# Check logs
type server_debug.log
```