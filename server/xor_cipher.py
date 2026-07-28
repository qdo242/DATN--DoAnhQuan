"""
XOR Cipher - Ma hoa XOR don gian
Dung de so sanh hieu nang voi AES-128-CBC
Luu y: XOR KHONG bao mat, chi phu hop test tham khao
"""

import os
import json
import time

NETWORK_KEY = b"ABC123"

def xor_encrypt(data: bytes) -> bytes:
    """Ma hoa XOR voi key."""
    key_len = len(NETWORK_KEY)
    return bytes(data[i] ^ NETWORK_KEY[i % key_len] for i in range(len(data)))

def xor_decrypt(data: bytes) -> bytes:
    """Giai ma XOR (phep nguoc lai cua encrypt)."""
    return xor_encrypt(data)

def make_sensor_payload(device_id, temp, humidity, pressure, co2, co, nh3, lat, lon, alt, sats, gw, seq):
    """Tao JSON payload tu du lieu cam bien (giong Wokwi)."""
    data = {
        "id": device_id,
        "t": temp,
        "h": humidity,
        "p": pressure,
        "co2": co2,
        "co": co,
        "nh3": nh3,
        "lat": lat,
        "lon": lon,
        "alt": alt,
        "sats": sats,
        "gw": gw,
        "seq": seq
    }
    return json.dumps(data, separators=(',', ':')).encode('utf-8')

def xor_encrypt_payload(payload: bytes) -> bytes:
    """Ma hoa payload, them IV 16 byte de giong AES."""
    iv = os.urandom(16)
    ciphertext = xor_encrypt(payload)
    return iv + ciphertext

def xor_decrypt_payload(packet: bytes) -> bytes:
    """Giai ma payload, bo qua IV 16 byte dau."""
    ciphertext = packet[16:]
    return xor_decrypt(ciphertext)

def bench_xor(data, iterations=2000):
    """Do thoi gian XOR encrypt."""
    times = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        xor_encrypt(data)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1_000_000)
    return sum(times) / len(times)

if __name__ == "__main__":
    print("=" * 50)
    print("XOR CIPHER - SO SANH VOI AES")
    print("=" * 50)
    
    # Tao payload giong Wokwi
    payload = make_sensor_payload(
        device_id="Xi_01",
        temp=28.5,
        humidity=62.3,
        pressure=1013.2,
        co2=420,
        co=3.5,
        nh3=2.1,
        lat=21.845,
        lon=104.098,
        alt=10.5,
        sats=8,
        gw="Y_01",
        seq=1001
    )
    
    print(f"\nPayload ({len(payload)} bytes):")
    print(f"  {payload.decode()}")
    
    # XOR encrypt/decrypt
    ct = xor_encrypt(payload)
    pt = xor_decrypt(ct)
    
    print(f"\nCiphertext: {ct.hex()[:64]}...")
    print(f"Decrypted:  {pt.decode()}")
    
    # Kiem tra
    assert payload == pt, "XOR failed!"
    print("\nXOR OK: (X XOR K) XOR K = X")
    
    # Do thoi gian
    avg_us = bench_xor(payload)
    print(f"\nThoi gian trung binh: {avg_us:.2f} us")
    
    # So sanh kich thuoc
    print(f"\nKich thuoc:")
    print(f"  Plaintext:  {len(payload)} bytes")
    print(f"  Ciphertext: {len(ct)} bytes")
    print(f"  Tang them:   {len(ct) - len(payload)} bytes (IV)")
    
    print("\n" + "=" * 50)
    print("Luu y: XOR KHONG bao mat!")
    print("Chi dung de so sanh hieu nang voi AES")
    print("=" * 50)