"""
MAIN_TEST.PY - Script Test Nhanh Server
=========================================
Gui 2 goi tin mau len server va kiem tra phan hoi HTTP 200.

Quy trinh:
  1. Lam sach du lieu telemetry cu
  2. Tao goi tin ma hoa AES-128-CBC
  3. Gui len server qua HTTP POST
  4. Kiem tra phan hoi

Chay: python main_test.py
"""

import requests
import json
import secrets
import sqlite3
import os
from Cryptodome.Cipher import AES

# ============================================================
# CAU HINH
# ============================================================
SERVER_URL = "http://127.0.0.1:5000/receive-data"
DB_NAME = os.path.join(os.path.dirname(__file__), '..', 'iot_security.db')
NETWORK_KEY = b'key_x_1234567890'

def make_packet(device_id, temp, humid, seq, lat=21.00355, lon=105.84255):
    """
    Tao goi tin ma hoa AES-128-CBC.

    Quy trinh:
      1. Tao JSON payload tu du lieu cam bien
      2. Padding duoi (\\0) cho du 16 byte
      3. Tao IV ngau nhien 16 byte
      4. Ma hoa AES-CBC
      5. Tra ve: IV + ciphertext (bytes)

    Args:
        device_id: Ma thiet bi (vi du: "Xi_01")
        temp: Nhiet do (do C)
        humid: Do am (%)
        seq: Sequence number
        lat: Vi do (mac dinh: 21.00355)
        lon: Kinh do (mac dinh: 105.84255)

    Returns:
        bytes: IV (16 byte) + ciphertext
    """
    # Tao JSON payload
    data = {
        "id": device_id,
        "t": temp,
        "h": humid,
        "co2": 420,
        "co": 5.0,
        "nh3": 2.0,
        "lat": lat,
        "lon": lon,
        "seq": seq
    }
    plaintext = json.dumps(data).encode('utf-8')

    # Padding duoi (\\0) cho du 16 byte
    padded_len = len(plaintext)
    if padded_len % 16 != 0:
        padded_len = ((padded_len // 16) + 1) * 16
    padded_plaintext = plaintext.ljust(padded_len, b'\0')

    # Tao IV ngau nhien 16 byte
    iv = secrets.token_bytes(16)

    # Ma hoa AES-128-CBC
    cipher = AES.new(NETWORK_KEY, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(padded_plaintext)

    # Tra ve IV + ciphertext
    return iv + ciphertext

def reset_db():
    """
    Lam sach du lieu telemetry trong database.
    Giu nguyen bang devices de thiet bi khong bi mat.
    """
    if os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        conn.execute("DELETE FROM telemetry")
        conn.commit()
        conn.close()
        print("[*] Da lam sach du lieu telemetry.\n")

if __name__ == "__main__":
    reset_db()
    print("=== GUI THU DU LIEU LEN SERVER ===\n")

    # Gui goi tin tu Xi_01
    packet = make_packet("Xi_01", 25.0, 60.0, 1)
    r = requests.post(SERVER_URL, json={"payload": packet.hex()})
    print(f"Xi_01: {r.status_code} - {r.json()}")

    # Gui goi tin tu Xi_02
    packet2 = make_packet("Xi_02", 30.0, 70.0, 1)
    r2 = requests.post(SERVER_URL, json={"payload": packet2.hex()})
    print(f"Xi_02: {r2.status_code} - {r2.json()}")

    print("\nDa gui xong. Hay mo Dashboard de kiem tra.")