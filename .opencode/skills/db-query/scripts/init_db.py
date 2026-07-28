#!/usr/bin/env python3
"""Initialize the SQLite database with 3 devices."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'iot_security.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create devices table
    c.execute('''CREATE TABLE IF NOT EXISTS devices (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Create telemetry table
    c.execute('''CREATE TABLE IF NOT EXISTS telemetry (
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
    )''')
    
    # Create benchmark table
    c.execute('''CREATE TABLE IF NOT EXISTS benchmark (
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
    )''')
    
    # Insert default devices
    devices = [
        ('Xi_01', 'ESP32 Sensor 1', 'sensor'),
        ('Xi_02', 'ESP32 Sensor 2', 'sensor'),
        ('Y_01', 'Gateway', 'gateway')
    ]
    
    for dev in devices:
        c.execute('INSERT OR IGNORE INTO devices VALUES (?, ?, ?, CURRENT_TIMESTAMP)', dev)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")
    print("Devices: Xi_01, Xi_02, Y_01")

if __name__ == '__main__':
    init_db()