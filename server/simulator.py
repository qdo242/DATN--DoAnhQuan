"""
SIMULATOR.PY - Mo Phong Luong Du Lieu
=======================================
Mo phong toan bo luong du lieu:
  Xi (ESP32) -> LoRa -> Y Gateway -> Server

Script mo phong:
  1. Xi phat Beacon qua LoRa
  2. Y Gateway nhan va tra ACK
  3. Xi doc cam bien, tao JSON
  4. Xi ma hoa AES-128-CBC
  5. Xi gui qua LoRa sang Y Gateway
  6. Y Gateway chuyen tiep len Server qua HTTP

Chay: python simulator.py
"""

import requests
import json
import secrets
import time
from Cryptodome.Cipher import AES

# ============================================================
# CAU HINH
# ============================================================
NETWORK_KEY = b'key_x_1234567890'  # Key ma hoa AES (16 byte)
SERVER_URL = "http://127.0.0.1:5000/receive-data"  # Server endpoint

def simulate_xi_to_y_to_server(device_id, start_lat, start_lon):
    """
    Mo phong luong du lieu tu Xi den Y Gateway den Server.

    Args:
        device_id: Ma thiet bi (vi du: "Xi_01")
        start_lat: Vi do ban dau
        start_lon: Kinh do ban dau
    """
    print(f"\n{'='*50}")
    print(f"=== KHOI DONG THIET BI {device_id} ===")
    print(f"{'='*50}")

    curr_lat, curr_lon = start_lat, start_lon

    # Chay 5 chu ky
    for seq in range(1, 6):
        print(f"\n--- Chu ky {seq} ---")

        # ---- GIAI DOAN 1: BEACON/ACK ----
        # Xi phat Beacon qua LoRa
        print(f"[{device_id}] Phat Beacon LoRa...")
        time.sleep(1)

        # Y Gateway nhan Beacon va tra ACK
        print(f"[GATEWAY Y] Nhan Beacon tu {device_id}, gui ACK")
        print(f"[{device_id}] Nhan ACK, bat dau truyen tin.")

        # ---- GIAI DOAN 2: DOC CAM BIEN ----
        # Doc gia tri cam bien ngau nhien (mo phong BME280 + MQ-135)
        temp = round(28.0 + (secrets.randbelow(100) / 10.0), 1)  # 28.0 - 38.0 do C
        humi = round(60.0 + (secrets.randbelow(100) / 10.0), 1)  # 60.0 - 70.0 %
        co = round(5.0 + (secrets.randbelow(30) / 10.0), 1)      # 5.0 - 8.0 ppm
        co2 = 400 + secrets.randbelow(50)                          # 400 - 450 ppm
        nh3 = round(2.0 + (secrets.randbelow(20) / 10.0), 1)     # 2.0 - 4.0 ppm

        # Cap nhat toa do GPS (mo phong di chuyen)
        curr_lat += 0.0001
        curr_lon += 0.0001

        # Tao JSON payload
        data = {
            "id": device_id,
            "t": temp,
            "h": humi,
            "co": co,
            "co2": co2,
            "nh3": nh3,
            "lat": round(curr_lat, 5),
            "lon": round(curr_lon, 5),
            "seq": seq
        }
        print(f"[{device_id}] Du lieu: {data}")

        # ---- GIAI DOAN 3: MA HOA AES-128-CBC ----
        # Chuyen JSON thanh bytes
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

        # ---- GIAI DOAN 4: GUI QUA LoRa SANG GATEWAY ----
        print(f"[{device_id}] Gui du lieu ma hoa ({len(ciphertext)} bytes) qua LoRa...")
        time.sleep(0.5)

        # Y Gateway nhan du lieu tu Xi
        print(f"[GATEWAY Y] Nhan du lieu ma hoa tu {device_id}")

        # ---- GIAI DOAN 5: GATEWAY CHUYEN TIEP LEN SERVER ----
        # Dong goi: IV + ciphertext -> hex string
        payload_hex = (iv + ciphertext).hex()
        print(f"[GATEWAY Y] Chuyen tiep len Server...")

        # Gui HTTP POST len Server
        try:
            r = requests.post(SERVER_URL, json={"payload": payload_hex}, timeout=10)
            print(f"[SERVER] Phan hoi: {r.status_code} - {r.json()}")
            if r.status_code == 200:
                print(f"[GATEWAY Y] Gui ACK cho {device_id}")
        except Exception as e:
            print(f"[!] LOI: Khong ket noi duoc Server! ({e})")

        time.sleep(2)

if __name__ == "__main__":
    print("=== MO PHONG LUONG XI -> Y (GATEWAY) -> SERVER ===\n")

    # Mo phong Xi_01
    simulate_xi_to_y_to_server("Xi_01", 21.84470, 104.09700)

    print("\n" + "="*50)

    # Mo phong Xi_02
    simulate_xi_to_y_to_server("Xi_02", 21.84550, 104.09820)

    print("\n=== KET THUC ===")