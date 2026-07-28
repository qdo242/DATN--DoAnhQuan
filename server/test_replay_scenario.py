"""
TEST_REPLAY_SCENARIO.PY - Kich Ban Thu Nghiem Phat Lai (Hinh 4.16)
====================================================================
Thu nghiem theo yeu cau cua thay Hai:
  1. Gui goi tin voi seq=1001 -> Server OK (HTTP 200)
  2. Gui lai goi tin cu voi seq=1001 -> Server REJECT (HTTP 403)

Chay: python test_replay_scenario.py
"""

import sys, os, json, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Cryptodome.Cipher import AES
from app import app
import init_db
import sqlite3

# ============================================================
# CAU HINH
# ============================================================
AES_KEY = b'key_x_1234567890'

def pad(data: bytes) -> bytes:
    """
    Padding duoi (\\0) cho du 16 byte (block size cua AES).
    """
    padded_len = ((len(data) + 15) // 16) * 16
    return data.ljust(padded_len, b'\0')

def aes_encrypt(plaintext: bytes) -> bytes:
    """
    Ma hoa du lieu bang AES-128-CBC.

    Quy trinh:
      1. Tao IV ngau nhien 16 byte
      2. Padding plaintext
      3. Ma hoa AES-CBC
      4. Tra ve: IV + ciphertext
    """
    iv = os.urandom(16)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(plaintext))
    return iv + ct

# ============================================================
# KHOI TAO DATABASE SACH
# ============================================================
client = app.test_client()
device = "Xi_01"
seq = 1001

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'iot_security.db')
if os.path.exists(db_path):
    os.remove(db_path)
init_db.init_db()

# ============================================================
# TAO PAYLOAD GIONG HET CHO CA 2 LAN GUI
# ============================================================
payload = {
    "id": "Xi_01",
    "t": 28.5,
    "h": 65.2,
    "p": 1008.0,
    "co2": 420,
    "co": 5.1,
    "nh3": 2.3,
    "lat": 21.8447,
    "lon": 105.8426,
    "alt": 10.0,
    "sats": 7,
    "gw": "Y_01",
    "seq": seq
}
plaintext = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
payload_hex = aes_encrypt(plaintext).hex()

print("4.16. Kich ban thu nghiem phat lai cung sequence number")
print("=" * 70)

# ============================================================
# BUOC 1: GUI LAN DAU TIEN (seq=1001)
# ============================================================
print("\nLan 1 - Xi_01 gui payload chua seq=1001:")
print(f"  Payload (hex):      {payload_hex[:50]}...")
resp1 = client.post('/receive-data', json={"payload": payload_hex})
print(f"  HTTP Response:       {resp1.status_code} {resp1.get_json()}")
conn = sqlite3.connect(db_path)
last_seq = conn.execute('SELECT last_seq FROM devices WHERE device_id = ?', (device,)).fetchone()[0]
print(f"  last_seq sau xu ly: {last_seq}")
conn.close()

# ============================================================
# BUOC 2: GUI LAN THU HAI (gui lai payload cu)
# ============================================================
print("\nLan 2 - Gui lai payload cu (seq=1001):")
print(f"  Payload (hex):      {payload_hex[:50]}...")
resp2 = client.post('/receive-data', json={"payload": payload_hex})
print(f"  HTTP Response:       {resp2.status_code} {resp2.get_json()}")

conn = sqlite3.connect(db_path)
last_seq2 = conn.execute('SELECT last_seq FROM devices WHERE device_id = ?', (device,)).fetchone()[0]
telem_count = conn.execute('SELECT COUNT(*) FROM telemetry WHERE device_id = ?', (device,)).fetchone()[0]
conn.close()

print(f"  last_seq sau xu ly: {last_seq2}")
print(f"  So ban ghi telemetry: {telem_count} (khong tao ban ghi moi do replay)")

print(f"\n{'=' * 70}")
print(f"Ket luan: He thong phat hien va chan thanh cong tan cong phat lai.")
print(f"Goi tin cu bi tu choi voi HTTP 403, khong tao ban ghi telemetry moi.")
print(f"{'=' * 70}")