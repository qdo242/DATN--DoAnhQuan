"""
VERIFY_WOKWI.PY - Kiem Tra Cau Hinh Wokwi-Server
===================================================
Kiem tra Wokwi va Server da khop noi chinh xac chua.

Script kiem tra:
  1. Tao du lieu giong sketch.ino
  2. Ma hoa AES-128-CBC (giong ESP32)
  3. Gui len Server
  4. Kiem tra Server giai ma dung

Chay: python verify_wokwi.py
"""

import requests
import sqlite3
import os
from Cryptodome.Cipher import AES
import json
import secrets

# ============================================================
# CAU HINH
# ============================================================
NETWORK_KEY = b'key_x_1234567890'  # Key ma hoa AES (16 byte)
SERVER_URL = "http://127.0.0.1:5000/receive-data"

def simulate_wokwi_cpp_logic(node_id):
    """
    Mo phong chinh xac AES-128-CBC trong sketch.ino.

    Args:
        node_id: Ma thiet bi (vi du: "Xi_01")

    Returns:
        bool: True neu thanh cong, False neu that bai
    """
    print(f"--- Dang kiem tra Node: {node_id} ---")

    # ---- BUOC 1: TAO DATA GIONG ESP32 ----
    data = {
        "id": node_id,
        "t": 25.5,
        "h": 60.0,
        "co2": 420,
        "co": 5.0,
        "nh3": 2.0,
        "lat": 21.0045,
        "lon": 105.8433,
        "seq": 999
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
    final_payload = (iv + ciphertext).hex()

    # ---- BUOC 5: GUI LEN SERVER ----
    try:
        r = requests.post(SERVER_URL, json={"payload": final_payload})
        print(f"Ket qua: {r.status_code} - {r.json()}\n")
        return r.status_code == 200
    except Exception as e:
        print(f"Loi ket noi Server: {e}")
        return False

if __name__ == "__main__":
    print("=== BAT DAU KIEM DINH TU DONG CAU HINH WOKWI-SERVER ===\n")

    # Kiem tra Xi_01
    success = simulate_wokwi_cpp_logic("Xi_01")

    if success:
        print("=> CHUC MUNG: Cau hinh Wokwi va Server da khop noi hoan hao!")
    else:
        print("=> CANH BAO: Co loi trong viec khop noi cau hinh.")