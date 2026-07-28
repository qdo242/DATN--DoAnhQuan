import time
import statistics
import json
import os
import sqlite3
import random
from Cryptodome.Cipher import AES
from xor_cipher import xor_encrypt, xor_decrypt, NETWORK_KEY as XOR_KEY

AES_KEY = b'key_x_1234567890'
ITERATIONS = 2000

# ===== DOC DU LIEU TU DATABASE (AES tu Wokwi/Server) =====
db_path = os.path.join(os.path.dirname(__file__), '..', 'iot_security.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT id, device_id, decrypt_ms, seq_ms, log_ms, total_ms, status FROM benchmark ORDER BY id").fetchall()
    conn.close()
    print("=" * 70)
    print("  DU LIEU TU DATABASE (AES tu Wokwi/Server)")
    print("=" * 70)
    print(f"{'ID':<4} {'Device':<10} {'Decrypt':<10} {'Seq':<10} {'Log':<10} {'Total':<10} {'Status':<8}")
    print("-" * 62)
    for r in rows:
        print(f"{r[0]:<4} {r[1]:<10} {r[2]:<10.3f} {r[3]:<10.3f} {r[4]:<10.3f} {r[5]:<10.3f} {r[6]:<8}")
    if rows:
        avg_d = statistics.mean([r[2] for r in rows])
        avg_s = statistics.mean([r[3] for r in rows])
        avg_l = statistics.mean([r[4] for r in rows])
        avg_t = statistics.mean([r[5] for r in rows])
        ok = sum(1 for r in rows if r[6] == 'OK')
        fail = sum(1 for r in rows if r[6] == 'FAIL')
        print(f"\nTrung binh: Decrypt={avg_d:.3f}ms Seq={avg_s:.3f}ms Log={avg_l:.3f}ms Total={avg_t:.3f}ms")
        print(f"Thanh cong: {ok} | Replay bi chan: {fail}")
    print()

# ===== TAO DU LIEU JSON TUONG TU WOKWI =====
def make_wokwi_payload(seq):
    """Tao JSON payload giong nhu Wokwi gui"""
    return {
        "id": f"Xi_{random.randint(1,2):02d}",
        "t": round(random.uniform(25, 31), 1),
        "h": round(random.uniform(58, 65), 1),
        "p": round(random.uniform(1005, 1035), 1),
        "co2": random.randint(380, 450),
        "co": round(random.uniform(2, 8), 1),
        "nh3": round(random.uniform(1, 5), 1),
        "lat": round(random.uniform(21.844, 21.846), 5),
        "lon": round(random.uniform(104.097, 104.099), 5),
        "alt": round(random.uniform(8, 15), 1),
        "sats": random.randint(5, 12),
        "gw": "Y_01",
        "seq": seq
    }

# Tao 5 mau JSON voi kich thuoc tang dan
sample_payloads = []
for i, seq in enumerate([1001, 1050, 1100, 1500, 2000]):
    data = make_wokwi_payload(seq)
    json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    sample_payloads.append((len(json_str), json_str.encode('utf-8')))

print("=" * 70)
print("  MAU JSON TUONG TU WOKWI")
print("=" * 70)
for size, payload in sample_payloads:
    print(f"  {size:3d}B: {payload[:80].decode('utf-8')}...")
print()

def aes_encrypt(data: bytes) -> bytes:
    iv = os.urandom(16)
    padded_len = ((len(data) + 15) // 16) * 16
    pad = data.ljust(padded_len, b'\0')
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad)
    return iv + ct

def aes_decrypt(packet: bytes) -> bytes:
    iv = packet[:16]
    ct = packet[16:]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
    return cipher.decrypt(ct).rstrip(b'\0')

def xor_encrypt_wrapper(data: bytes) -> bytes:
    return xor_encrypt(data)

def xor_decrypt_wrapper(data: bytes) -> bytes:
    return xor_decrypt(data)

def bench(func, data, iters=ITERATIONS):
    times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        func(data)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1_000_000)
    return statistics.mean(times), statistics.stdev(times), min(times), max(times)

# ===== BENCHMARK VOI DU LIEU JSON TUONG TU WOKWI =====
results = []
print("=" * 70)
print("  BENCHMARK: AES vs XOR voi du lieu JSON tuong tu Wokwi")
print("=" * 70)

for size, pt in sample_payloads:
    ct_aes = aes_encrypt(pt)
    ct_xor = xor_encrypt_wrapper(pt)

    mean_e, std_e, min_e, max_e = bench(aes_encrypt, pt)
    mean_d, std_d, min_d, max_d = bench(aes_decrypt, ct_aes)
    mean_xe, std_xe, min_xe, max_xe = bench(xor_encrypt_wrapper, pt)
    mean_xd, std_xd, min_xd, max_xd = bench(xor_decrypt_wrapper, ct_xor)

    results.append((size, mean_e, std_e, mean_d, std_d, mean_xe, std_xe, mean_xd, std_xd))
    print(f"Payload {size:3d}B: AES enc={mean_e:8.2f}us dec={mean_d:8.2f}us | XOR enc={mean_xe:8.2f}us dec={mean_xd:8.2f}us")

print("\n=== BANG SO SANH CHI TIET ===")
header = f"{'Size':>6} | {'AES Enc(us)':>12} {'AES Dec(us)':>12} {'XOR Enc(us)':>12} {'XOR Dec(us)':>12} | {'Ty le AES/XOR':>14}"
print(header)
print("-" * len(header))
for size, me, se, md, sd, mxe, sxe, mxd, sxd in results:
    ratio = (me + md) / (mxe + mxd)
    print(f"{size:>6} | {me:>10.2f}us {md:>10.2f}us {mxe:>10.2f}us {mxd:>10.2f}us | {ratio:>12.1f}x")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
sizes_arr = np.array([r[0] for r in results])
aes_enc = np.array([r[1] for r in results])
aes_dec = np.array([r[3] for r in results])
xor_enc = np.array([r[5] for r in results])
xor_dec = np.array([r[7] for r in results])

x = np.arange(len(sizes_arr))
w = 0.2

ax1.bar(x - 1.5*w, aes_enc, w, label='AES Encrypt', color='#e74c3c')
ax1.bar(x - 0.5*w, aes_dec, w, label='AES Decrypt', color='#c0392b')
ax1.bar(x + 0.5*w, xor_enc, w, label='XOR Encrypt', color='#2ecc71')
ax1.bar(x + 1.5*w, xor_dec, w, label='XOR Decrypt', color='#27ae60')
ax1.set_xticks(x)
ax1.set_xticklabels([f'{s}B' for s in sizes_arr])
ax1.set_ylabel('Thoi gian (microseconds)')
ax1.set_title('So sanh toc do AES vs XOR (du lieu JSON Wokwi)')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

ax2.bar(x - 1.5*w, aes_enc + aes_dec, w, label='AES (Enc+Dec)', color='#e74c3c')
ax2.bar(x + 0.5*w, xor_enc + xor_dec, w, label='XOR (Enc+Dec)', color='#2ecc71')
ax2.set_xticks(x)
ax2.set_xticklabels([f'{s}B' for s in sizes_arr])
ax2.set_ylabel('Tong thoi gian (microseconds)')
ax2.set_title('So sanh tong thoi gian xu ly')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'images', 'benchmark_crypto.png')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
plt.savefig(out_path, dpi=150)
print(f"\nDa luu bieu do: {os.path.basename(out_path)}")
plt.close()

# ===== SO SANH CUOI CUNG: AES tu DB vs XOR mo phong =====
print("\n" + "=" * 70)
print("  SO SANH: AES-128-CBC (du lieu thuc tu Server) vs XOR (mo phong)")
print("=" * 70)

# Lay gia tri AES trung binh tu DB neu co
if rows:
    aes_server_total = avg_t
    print(f"\nAES tu Server (Wokwi/Server): {aes_server_total:.3f} ms/request")
    print(f"  - Decrypt: {avg_d:.3f} ms")
    print(f"  - Seq check: {avg_s:.3f} ms")
    print(f"  - DB write: {avg_l:.3f} ms")
else:
    aes_server_total = None

print(f"\n{'Size':<8} {'AES(us)':<12} {'XOR(us)':<12} {'Ty le':<10}")
print("-" * 42)
for size, me, se, md, sd, mxe, sxe, mxd, sxd in results:
    aes_total = me + md
    xor_total = mxe + mxd
    ratio = xor_total / aes_total if aes_total > 0 else 0
    print(f"{size:<8} {aes_total:<12.2f} {xor_total:<12.2f} {ratio:<10.1f}x")
print("=" * 70)
