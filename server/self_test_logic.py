"""
SELF_TEST_LOGIC.PY - Tu Kiem Dinh Logic He Thong
==================================================
Kiem tra toan bo luong du lieu:
  Wokwi (ESP32) -> AES encrypt -> Server -> Decrypt -> Database

Script kiem tra:
  1. Tao JSON payload giong sketch.ino
  2. Ma hoa AES-128-CBC (giong ESP32)
  3. Gui len Server
  4. Kiem tra Server giai ma dung
  5. Xac nhan du lieu luu trong Database

Chay: python self_test_logic.py
"""

import os
import sqlite3
import json
import secrets
from Cryptodome.Cipher import AES
from app import app, get_db_connection

# ============================================================
# CAU HINH
# ============================================================
NETWORK_KEY = b'key_x_1234567890'  # Key ma hoa AES (16 byte)

def test_full_system_logic():
    """
    Kiem tra toan bo logic he thong.

    Quy trinh:
      1. Tao JSON payload giong sketch.ino
      2. Padding duoi (\\0) cho du 16 byte
      3. Tao IV ngau nhien 16 byte
      4. Ma hoa AES-128-CBC
      5. Gui len Server
      6. Kiem tra Server giai ma dung
      7. Xac nhan du lieu luu trong Database
    """
    print("=== BAT DAU KIEM DINH LOGIC HE THONG WOKWI -> SERVER ===\n")

    node_id = "Xi_01"

    # ---- BUOC 1: TAO JSON PAYLOAD ----
    # Giong nhu sketch.ino gui tu ESP32
    data = {
        "id": node_id,
        "t": 28.5,
        "h": 60.0,
        "p": 1005.0,
        "co2": 420,
        "co": 5.0,
        "nh3": 2.0,
        "lat": 21.0045,
        "lon": 105.8433,
        "alt": 10,
        "sats": 8,
        "gw": "Y_01",
        "seq": 50
    }
    plaintext = json.dumps(data).encode('utf-8')

    # ---- BUOC 2: PADDING ----
    # Giong sketch.ino: memset(0) truoc khi ma hoa
    padded_len = len(plaintext)
    if padded_len % 16 != 0:
        padded_len = ((padded_len // 16) + 1) * 16
    padded_plaintext = plaintext.ljust(padded_len, b'\0')

    # ---- BUOC 3: MA HOA AES-128-CBC ----
    iv = secrets.token_bytes(16)  # IV ngau nhien 16 byte
    cipher = AES.new(NETWORK_KEY, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(padded_plaintext)

    # ---- BUOC 4: DONG GOI HEX ----
    # Packet = IV (16 byte) + ciphertext
    final_hex_payload = (iv + ciphertext).hex()
    print(f"[Xi] Da tao goi tin ma hoa (Hex): {final_hex_payload[:50]}...\n")

    # ---- BUOC 5: GUI LEN SERVER ----
    with app.test_client() as client:
        print("[Server] Dang tiep nhan va giai ma...")
        response = client.post('/receive-data', json={"payload": final_hex_payload})

        print(f"[Server] Ket qua phan hoi: {response.status_code}")
        print(f"[Server] Du lieu tra ve: {response.get_json()}")

        # ---- BUOC 6: KIEM TRA KET QUA ----
        if response.status_code == 200:
            print("\n=> KET LUAN: Code Wokwi va Server da khop noi thanh cong!")

            # Xac nhan du lieu luu trong Database
            conn = get_db_connection()
            log = conn.execute(
                'SELECT * FROM telemetry WHERE device_id = ? ORDER BY id DESC LIMIT 1',
                (node_id,)
            ).fetchone()
            conn.close()

            if log:
                print(f"[*] Xac nhan Database da luu: Nhiet do={log['temperature']}")
        else:
            print("\n=> KET LUAN: Co loi trong logic giai ma.")

if __name__ == "__main__":
    test_full_system_logic()