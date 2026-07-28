"""
INIT_DB.PY - Khoi tao Database
================================
Tao moi SQLite database voi 3 bang:
  - devices: Danh sach thiet bi
  - telemetry: Du lieu cam bien
  - benchmark: Ket qua do hieu nang

Chay: python init_db.py
"""

import sqlite3
import os

# Duong dan database (cung thu muc voi server/)
DB_NAME = os.path.join(os.path.dirname(__file__), '..', 'iot_security.db')

def init_db():
    """
    Khoi tao database moi.
    
    Quy trinh:
      1. Xoa database cu (neu co)
      2. Tao 3 bang: devices, telemetry, benchmark
      3. Them 3 thiet bi mac dinh: Xi_01, Xi_02, Y_01
    """
    # Xoa database cu de bat dau moi
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    # Tao ket noi moi
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ============================================================
    # BANG 1: DEVICES - Danh sach thiet bi
    # ============================================================
    # device_id: Ma thiet bi (primary key)
    # network_key: Key ma hoa AES (16 byte)
    # last_seq: Sequence cuoi cung (dung de chong replay)
    # latitude, longitude: Vi tri GPS mac dinh
    # description: Mo ta thiet bi
    cursor.execute('''CREATE TABLE devices (
        device_id TEXT PRIMARY KEY,
        network_key TEXT NOT NULL,
        last_seq INTEGER DEFAULT -1,
        latitude REAL,
        longitude REAL,
        description TEXT
    )''')

    # ============================================================
    # BANG 2: TELEMETRY - Du lieu cam bien
    # ============================================================
    # id: Ma tu tang
    # device_id: Ma thiet bi (foreign key)
    # timestamp: Thoi gian nhan du lieu (mac dinh = CURRENT_TIMESTAMP)
    # temperature, humidity, pressure: Cam bien BME280
    # co2, co, nh3: Cam bien khi khi
    # altitude, satellites: GPS
    # latitude, longitude: Toa do GPS
    # status: "An toan" hoac "Canh bao: ..."
    cursor.execute('''CREATE TABLE telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL,
        pressure REAL,
        co2 REAL,
        co REAL,
        nh3 REAL,
        altitude REAL,
        satellites INTEGER,
        latitude REAL,
        longitude REAL,
        status TEXT,
        FOREIGN KEY (device_id) REFERENCES devices (device_id)
    )''')

    # ============================================================
    # BANG 3: BENCHMARK - Ket qua do hieu nang
    # ============================================================
    # id: Ma tu tang
    # device_id: Ma thiet bi
    # decrypt_ms: Thoi gian giai ma (ms)
    # seq_ms: Thoi gian kiem tra seq (ms)
    # log_ms: Thoi gian ghi log (ms)
    # total_ms: Tong thoi gian xu ly (ms)
    # status: "OK" hoac "FAIL"
    # timestamp: Thoi gian ghi nhan
    cursor.execute('''CREATE TABLE benchmark (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        decrypt_ms REAL,
        seq_ms REAL,
        log_ms REAL,
        total_ms REAL,
        status TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # ============================================================
    # THEM THIET BI MAC DINH
    # ============================================================
    # Key chung cho ca he thong: key_x_1234567890 (16 byte)
    # last_seq = -1: Chua nhan goi tin nao
    # Toa do GPS: Mu Cang Chai, Yen Bai, Viet Nam
    common_key = "key_x_1234567890"
    devices_data = [
        ('Xi_01', common_key, -1, 21.84470, 104.09700, 'Node cam bien Xi_01 - Mu Cang Chai'),
        ('Xi_02', common_key, -1, 21.84550, 104.09820, 'Node cam bien Xi_02 - Mu Cang Chai'),
        ('Y_01',  common_key, -1, 21.84510, 104.09750, 'Gateway Y_01 - Mu Cang Chai')
    ]

    # Them 3 thiet bi vao bang devices
    cursor.executemany(
        "INSERT INTO devices (device_id, network_key, last_seq, latitude, longitude, description) VALUES (?,?,?,?,?,?)",
        devices_data
    )

    conn.commit()
    conn.close()
    print("Da khoi tao database thanh cong.")
    print("3 thiet bi: Xi_01, Xi_02, Y_01")

if __name__ == "__main__":
    init_db()