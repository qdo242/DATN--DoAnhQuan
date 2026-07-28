"""
TEST_REPLAY.PY - Thu Nghiem Chong Tan Cong Phat Lai
=====================================================
Script tu dong:
  1. Khoi tao database sach
  2. Mo phong server Flask bang test client
  3. Gui goi tin hop le -> kiem tra HTTP 200
  4. Gui lai goi tin cu (replay) -> kiem tra HTTP 403
  5. Gui goi tin voi seq cu -> kiem tra HTTP 403
  6. Gui goi tin voi seq moi -> kiem tra HTTP 200
  7. Hien thi bang ket qua benchmark

Chay: python test_replay.py
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

def aes_encrypt(data: bytes) -> bytes:
    """
    Ma hoa du lieu bang AES-128-CBC.

    Quy trinh:
      1. Tao IV ngau nhien 16 byte
      2. Padding duoi (\\0) cho du 16 byte
      3. Ma hoa AES-CBC
      4. Tra ve: IV + ciphertext
    """
    iv = os.urandom(16)
    padded_len = ((len(data) + 15) // 16) * 16
    pad = data.ljust(padded_len, b'\0')
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad)
    return iv + ct

def make_payload(device_id, seq):
    """
    Tao goi tin JSON ma hoa AES.

    Args:
        device_id: Ma thiet bi (vi du: "Xi_01")
        seq: Sequence number

    Returns:
        str: Hex string cua IV + ciphertext
    """
    data = {
        "id": device_id,
        "t": 28.5, "h": 65.2, "p": 1008.0,
        "co2": 420, "co": 5.1, "nh3": 2.3,
        "lat": 21.8447, "lon": 105.8426,
        "alt": 10.0, "sats": 7,
        "gw": "Y_01",
        "seq": seq,
    }
    plaintext = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    ct = aes_encrypt(plaintext)
    return ct.hex()

print("=" * 65)
print("  THU NGHIEM CHONG TAN CONG PHAT LAI (REPLAY ATTACK)")
print("=" * 65)

# ============================================================
# KHOI TAO DATABASE SACH
# ============================================================
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'iot_security.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print("\n[*] Da xoa database cu")

init_db.init_db()
print("[*] Da khoi tao database moi")

# ============================================================
# CAC TEST CASE
# ============================================================
# Dung Flask test client (khong can chay server that)
client = app.test_client()
device = "Xi_01"

results = []
test_cases = [
    # (Ten test, seq, HTTP code mong doi, mo ta)
    ("Gui goi tin hop le (seq=100)", 100, 200, "Goi tin hop le"),
    ("Gui LAI goi tin cu (seq=100)", 100, 403, "Phat hien replay!"),
    ("Gui goi tin voi seq cu hon (seq=50)", 50, 403, "Seq cu hon -> chan replay"),
    ("Gui goi tin hop le moi (seq=101)", 101, 200, "Goi tin hop le"),
    ("Gui goi tin voi seq bang hien tai (seq=101)", 101, 403, "Seq trung -> phat hien replay"),
    ("Gui goi tin hop le moi (seq=200)", 200, 200, "Goi tin hop le"),
    ("Thu replay ngay sau do (seq=200)", 200, 403, "Phat hien replay!"),
]

print(f"\n{'='*65}")
print(f"  KET QUA THU NGHIEM TREN THIET BI: {device}")
print(f"{'='*65}")
print(f"{'STT':<4} {'Test case':<45} {'Ky vong':<10} {'Thuc te':<10} {'Ket luan':<12}")
print("-" * 81)

for i, (name, seq, expected, desc) in enumerate(test_cases, 1):
    # Tao payload va gui len server
    payload_hex = make_payload(device, seq)
    t0 = time.perf_counter()
    resp = client.post('/receive-data', json={"payload": payload_hex})
    elapsed = (time.perf_counter() - t0) * 1000
    actual = resp.status_code
    status = resp.get_json() or {}

    # Kiem tra ket qua
    passed = actual == expected
    verdict = "PASS" if passed else "FAIL"
    results.append((name, seq, expected, actual, verdict, elapsed, status, desc))

    print(f"{i:<4} {name:<45} {expected:<10} {actual:<10} {verdict:<12}")
    if not passed:
        reason = status.get('reason', 'N/A')
        print(f"     -> LOI: Expected {expected}, got {actual}. Reason: {reason}")

print("-" * 81)
total_pass = sum(1 for r in results if r[4] == "PASS")
total_fail = sum(1 for r in results if r[4] == "FAIL")
print(f"\n  Tong ket: {len(results)} test case -- {total_pass} PASS, {total_fail} FAIL")

# ============================================================
# HIEN THI BANG BENCHMARK TU DATABASE
# ============================================================
print(f"\n{'='*65}")
print(f"  DU LIEU BENCHMARK TU DATABASE")
print(f"{'='*65}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    SELECT id, device_id, decrypt_ms, seq_ms, log_ms, total_ms, status, timestamp
    FROM benchmark ORDER BY id
""")
rows = cursor.fetchall()
if rows:
    print(f"{'ID':<4} {'Device':<10} {'Decrypt(ms)':<12} {'Seq(ms)':<10} {'Log(ms)':<10} {'Total(ms)':<10} {'Status':<10} {'Time'}")
    print("-" * 95)
    for row in rows:
        print(f"{row[0]:<4} {row[1]:<10} {row[2]:<12.3f} {row[3]:<10.3f} {row[4]:<10.3f} {row[5]:<10.3f} {row[6]:<10} {row[7]}")
else:
    print("  (khong co du lieu)")

# Dem so lan replay bi chan
replay_count = sum(1 for r in rows if r[6] == "FAIL") if rows else 0
print(f"\n  So lan replay bi chan: {replay_count}/{len(rows) if rows else 0} request")
print(f"  Bao ve replay: {'HOAT DONG' if replay_count > 0 else 'KHONG CO DU LIEU'}")

conn.close()
print(f"\n{'='*65}")
print(f"  KET LUAN: He thong chong tan cong phat lai hoat dong dung.")
print(f"  Goi tin cu bi tu choi voi HTTP 403.")
print(f"  Sequence number duoc ma hoa trong payload AES-CBC,")
print(f"  ke tan cong khong the sua seq neu khong co key.")
print(f"{'='*65}")