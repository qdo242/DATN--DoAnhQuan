"""
CHECK_MY_SERVER.PY - Kiem Tra Ket Noi Server
==============================================
Script kiem tra nhanh:
  1. Server co dang chay khong
  2. Co the gui du lieu len server khong
  3. Server co giai ma duoc khong

Chay: python check_my_server.py
"""

import requests
import json
import secrets
from Cryptodome.Cipher import AES

# ============================================================
# CAU HINH
# ============================================================
NODE_ID = "IOT_NODE_01"  # Ma thiet bi (test)
NETWORK_KEY = b'key_x_1234567890'  # Key ma hoa AES (16 byte)
URL = "http://127.0.0.1:5000/receive-data"  # Server endpoint

def run_test():
    """
    Chay test kiem tra ket noi server.

    Quy trinh:
      1. Tao du lieu cam bien mau
      2. Ma hoa AES-128-CBC
      3. Gui HTTP POST len server
      4. Kiem tra phan hoi
    """
    print(f"[*] Dang kiem tra ket noi toi Server tai {URL}...")

    # ---- BUOC 1: TAO DU LIEU CAM BIEN MAU ----
    data = {
        "id": NODE_ID,
        "t": 26.5,
        "lat": 21.0045,
        "lon": 105.8433,
        "seq": 500
    }
    plaintext = json.dumps(data).encode('utf-8')

    # Padding duoi (\\0) cho du 16 byte
    padded_len = len(plaintext)
    if padded_len % 16 != 0:
        padded_len = ((padded_len // 16) + 1) * 16
    padded_plaintext = plaintext.ljust(padded_len, b'\0')

    # ---- BUOC 2: MA HOA AES-128-CBC ----
    iv = secrets.token_bytes(16)  # IV ngau nhien 16 byte
    cipher = AES.new(NETWORK_KEY, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(padded_plaintext)

    # ---- BUOC 3: DONG GOI VA GUI ----
    # Packet = IV (16 byte) + ciphertext
    packet = iv + ciphertext
    final_payload = packet.hex()  # Chuyen thanh hex string

    # ---- BUOC 4: GUI HTTP POST ----
    try:
        r = requests.post(URL, json={"payload": final_payload}, timeout=5)
        if r.status_code == 200:
            print("\n=> KET QUA: THANH CONG! Server da giai ma duoc du lieu.")
            print(f"Phan hoi tu Server: {r.json()}")
        else:
            print(f"\n=> KET QUA: THAT BAI (Code {r.status_code})")
            print(f"Ly do: {r.json().get('reason', 'Unknown error')}")
    except Exception as e:
        print(f"\n=> KET QUA: KHONG THE KET NOI TOI SERVER. ({e})")

if __name__ == "__main__":
    run_test()