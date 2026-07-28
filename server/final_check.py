"""
FINAL_CHECK.PY - Tu Kiem Dinh Truoc Khi Ban Giao
===================================================
Kiem tra he thong hoat dong dung truoc khi ban giao.

Script kiem tra:
  1. Tao du lieu cho Xi_01 va Y_01
  2. Ma hoa AES-128-CBC
  3. Gui len Server
  4. Kiem tra ca 2 thiet bi thanh cong

Chay: python final_check.py
"""

import json
import secrets
from Cryptodome.Cipher import AES
from app import app, get_db_connection

# ============================================================
# CAU HINH
# ============================================================
NETWORK_KEY = b'key_x_1234567890'  # Key ma hoa AES (16 byte)

def simulate_and_verify(node_id, data):
    """
    Mo phong va kiem tra 1 thiet bi.

    Args:
        node_id: Ma thiet bi (vi du: "Xi_01")
        data: Du lieu cam bien (dict)

    Returns:
        tuple: (status_code, response_json)
    """
    print(f"[*] Dang kiem dinh Node: {node_id}...")

    # ---- BUOC 1: CHUAN BI PLAINTEXT ----
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
    with app.test_client() as client:
        response = client.post('/receive-data', json={"payload": final_payload})
        return response.status_code, response.get_json()

if __name__ == "__main__":
    print("=== HE THONG TU KIEM DINH TRUOC KHI BAN GIAO ===\n")

    # Kiem tra Xi_01
    data_x = {"id": "Xi_01", "t": 28.2, "h": 60.0, "lat": 21.0045, "seq": 123}
    status_x, res_x = simulate_and_verify("Xi_01", data_x)
    print(f"Ket qua Node Xi_01: {status_x} - {res_x}\n")

    # Kiem tra Y_01
    data_y = {"id": "Y_01", "t": 30.5, "h": 70.0, "lat": 21.0065, "seq": 456}
    status_y, res_y = simulate_and_verify("Y_01", data_y)
    print(f"Ket qua Node Y_01: {status_y} - {res_y}\n")

    # Kiem tra ket qua
    if status_x == 200 and status_y == 200:
        print("=> CHUAN DOAN: He thong da san sang 100%. Hay mo Wokwi va chay ngay!")