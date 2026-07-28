"""
TEST_CBC.PY - Test AES-128-CBC voi Key Khac
==============================================
Test voi key khac (0x2B7E...) de kiem tra tinh linh hoat.

Luu y: Key nay KHAC voi key trong app.py (key_x_1234567890).
Chi dung de test, KHONG dung trong production.

Chay: python test_cbc.py
"""

import requests
import json
import secrets
from Cryptodome.Cipher import AES

# ============================================================
# CAU HINH
# ============================================================
NODE_ID = "IOT_NODE_01"

# Key khac voi app.py (chi dung de test)
NETWORK_KEY = bytes([0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6,
                     0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C])

URL = "http://127.0.0.1:5000/receive-data"

def run_test():
    """
    Chay test AES-128-CBC voi key khac.

    Quy trinh:
      1. Tao du lieu cam bien
      2. Ma hoa AES-128-CBC voi key khac
      3. Gui len Server
      4. Kiem tra phan hoi (mong doi: THAT BAI vi key khong khop)
    """
    print("=== BAT DAU KIEM DINH LOGIC WOKWI (AES-128-CBC) ===")

    # ---- BUOC 1: TAO DU LIEU CAM BIEN ----
    data = {
        "id": NODE_ID,
        "t": 28.5,
        "h": 60.0,
        "co2": 450,
        "lat": 21.00355,
        "lon": 105.84255,
        "seq": 100
    }
    plaintext = json.dumps(data).encode('utf-8')
    print(f"\n[ESP32] Du lieu tho: {plaintext.decode('utf-8')}")

    # ---- BUOC 2: PADDING ----
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
    packet = iv + ciphertext
    final_payload = packet.hex()
    print(f"[ESP32] Chuoi Hex gui di: {final_payload[:50]}...\n")

    # ---- BUOC 5: GUI LEN SERVER ----
    print("[Server] Dang tiep nhan va giai ma...")
    try:
        r = requests.post(URL, json={"payload": final_payload}, timeout=5)
        if r.status_code == 200:
            print("=> KET QUA: THANH CONG! Server da giai ma chinh xac.")
            print(f"Phan hoi tu Server: {r.json()}")
        else:
            print(f"=> KET QUA: THAT BAI (Code {r.status_code})")
            print(f"Ly do: {r.json().get('reason', 'Unknown error')}")
    except Exception as e:
        print(f"=> KET QUA: KHONG THE KET NOI TOI SERVER. ({e})")

if __name__ == "__main__":
    run_test()