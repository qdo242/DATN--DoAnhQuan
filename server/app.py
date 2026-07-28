"""
FLASK SERVER - IoT Security
============================
Server nhan du lieu ma hoa AES-128-CBC tu ESP32 (Wokwi/Hardware)
Thuc hien: giai ma, kiem tra replay attack, luu vao SQLite

API:
  POST /receive-data  - Nhan payload ma hoa tu Gateway
  GET  /benchmark     - Xem ket qua benchmark

Chay: python app.py
Server: http://0.0.0.0:5000
"""

# ============================================================
# IMPORT THU VIEN
# ============================================================
import os                    # Lam viec voi duong dan file
import sqlite3               # Ket noi SQLite database
from flask import Flask, request, jsonify  # Web framework
from Cryptodome.Cipher import AES  # Thu vien ma hoa AES (pycryptodome)
import json                  # Parse JSON
import logging               # Ghi log
import time                  # Do thoi gian xu ly
from concurrent.futures import ThreadPoolExecutor  # Chay song song

# ============================================================
# CAU HINH LOG
# ============================================================
# Ghi log vao file server_debug.log, level DEBUG (ghi tat ca)
logging.basicConfig(
    filename='server_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)

# ============================================================
# KHOI TAO FLASK APP
# ============================================================
app = Flask(__name__)

# Duong dan database (cung thu muc voi server/)
DB_NAME = os.path.join(os.path.dirname(__file__), '..', 'iot_security.db')

# Pre-Shared Key cho AES-128-CBC (16 byte)
# Phai giong voi key tren ESP32
NETWORK_KEY = b'key_x_1234567890'

# ThreadPool de chay ghi log song song (khong block request)
executor = ThreadPoolExecutor(max_workers=4)

# ============================================================
# HAM KET NOI DATABASE
# ============================================================
def get_db_connection():
    """
    Tao ket noi den SQLite database.
    row_factory = sqlite3.Row cho phep truy cap cot theo ten.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================
# HAM GIAI MA AES-128-CBC
# ============================================================
def verify_and_decrypt(raw_data):
    """
    Giai ma du lieu AES-128-CBC.
    
    Cau truc raw_data:
      - 16 byte dau: IV (Initialization Vector)
      - Phan con lai: ciphertext (du lieu da ma hoa)
    
    Quy trinh:
      1. Tach IV va ciphertext
      2. Tao cipher voi key + IV
      3. Decrypt ciphertext
      4. Bo padding (\0)
      5. Parse JSON
    
    Tra ve: (data, error)
      - data: dict neu thanh cong
      - error: string neu that bai
    """
    # Kiem tra do dai toi thieu: 16 (IV) + 16 (1 block AES)
    if len(raw_data) < 16 + 16:
        return None, "Packet too short"

    # Tach IV (16 byte dau) va ciphertext (phan con lai)
    iv = raw_data[:16]
    ciphertext = raw_data[16:]

    try:
        # Tao cipher AES-128-CBC voi key va IV
        cipher = AES.new(NETWORK_KEY, AES.MODE_CBC, iv=iv)
        
        # Giai ma va bo padding (\0 o cuoi)
        plaintext = cipher.decrypt(ciphertext).rstrip(b'\0')
        
        # Parse JSON thanh dict
        data = json.loads(plaintext.decode('utf-8'))
        return data, None
    except Exception as e:
        return None, f"Decryption Failed: {str(e)}"

# ============================================================
# HAM KIEM TRA REPLAY ATTACK
# ============================================================
def check_seq(device_id, seq):
    """
    Kiem tra replay attack bang sequence number.
    
    Nguyen tac:
      - Moi goi tin co seq (so thu tu) tang dan
      - Server luu last_seq cho tung thiet bi
      - Neu seq <= last_seq → Replay attack
    
    Tra ve: (ok, message)
      - ok: True neu hop le
      - message: thong bao loi neu bi tu choi
    """
    conn = get_db_connection()
    
    # Lay last_seq tu bang devices
    row = conn.execute(
        'SELECT last_seq FROM devices WHERE device_id = ?',
        (device_id,)
    ).fetchone()
    
    if row is None:
        conn.close()
        return False, "Device not found"
    
    # Kiem tra seq > last_seq
    if seq is not None and seq <= row['last_seq']:
        conn.close()
        return False, "Replay attack detected (seq <= last_seq)"
    
    conn.close()
    return True, None

# ============================================================
# HAM CAP NHAT SEQUENCE
# ============================================================
def update_seq(device_id, seq):
    """
    Cap nhat last_seq cho thiet bi trong database.
    
    Su dung retry 3 lan neu database bi locked.
    (SQLite chi cho phep 1 writer tai 1 thoi diem)
    """
    for attempt in range(3):
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE devices SET last_seq = ? WHERE device_id = ?',
                (seq, device_id)
            )
            conn.commit()
            conn.close()
            return
        except sqlite3.OperationalError as e:
            if 'locked' in str(e) and attempt < 2:
                time.sleep(0.1)  # Cho 100ms roi thu lai
                continue
            logging.error(f"DB update_seq failed: {e}")
            break

# ============================================================
# HAM GHI LOG TELEMERTY
# ============================================================
def log_telemetry(data, status):
    """
    Ghi du lieu cam bien vao bang telemetry.
    
    Du lieu gom:
      - device_id, temperature, humidity, pressure
      - co2, co, nh3 (khi khi)
      - altitude, satellites (GPS)
      - latitude, longitude (toa do)
      - status: "An toan" hoac "Canh bao: ..."
    
    Retry 3 lan neu database bi locked.
    """
    device_id = data.get('id', 'UNKNOWN')
    
    for attempt in range(3):
        try:
            conn = get_db_connection()
            
            # Lay toa do tu data hoac tu bang devices
            lat, lon = data.get('lat'), data.get('lon')
            if lat is None or lon is None:
                device = conn.execute(
                    'SELECT latitude, longitude FROM devices WHERE device_id = ?',
                    (device_id,)
                ).fetchone()
                if device:
                    lat, lon = device['latitude'], device['longitude']
            
            # Them du lieu vao bang telemetry
            conn.execute('''
                INSERT INTO telemetry
                    (device_id, temperature, humidity, pressure,
                     co2, co, nh3,
                     altitude, satellites,
                     latitude, longitude, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                device_id, data.get('t'), data.get('h'), data.get('p'),
                data.get('co2'), data.get('co'), data.get('nh3'),
                data.get('alt'), data.get('sats'),
                lat, lon, status
            ))
            conn.commit()
            conn.close()
            return
        except sqlite3.OperationalError as e:
            if 'locked' in str(e) and attempt < 2:
                time.sleep(0.1)
                continue
            logging.error(f"DB write failed: {e}")
            break

# ============================================================
# HAM LUU BENCHMARK
# ============================================================
def save_benchmark(device_id, decrypt_ms, seq_ms, log_ms, total_ms, status):
    """
    Luu ket qua benchmark vao database.
    
    Thong so do duoc:
      - decrypt_ms: Thoi gian giai ma (ms)
      - seq_ms: Thoi gian kiem tra seq (ms)
      - log_ms: Thoi gian ghi log (ms)
      - total_ms: Tong thoi gian xu ly (ms)
      - status: "OK" hoac "FAIL"
    
    Dung de phan tich hieu nang he thong.
    """
    for attempt in range(3):
        try:
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO benchmark
                    (device_id, decrypt_ms, seq_ms, log_ms, total_ms, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (device_id, decrypt_ms, seq_ms, log_ms, total_ms, status))
            conn.commit()
            conn.close()
            return
        except sqlite3.OperationalError as e:
            if 'locked' in str(e) and attempt < 2:
                time.sleep(0.1)
                continue
            break

# ============================================================
# API ENDPOINT: GET /benchmark
# ============================================================
@app.route('/benchmark', methods=['GET'])
def get_benchmark():
    """
    Lay ket qua benchmark tu database.
    
    Tra ve: JSON array voi 100 record gan nhat.
    Dung de xem hieu nang xu ly cua server.
    """
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT * FROM benchmark ORDER BY id DESC LIMIT 100
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ============================================================
# API ENDPOINT: POST /receive-data
# ============================================================
@app.route('/receive-data', methods=['POST'])
def receive_data():
    """
    Nhan du lieu ma hoa tu Gateway/ESP32.
    
    Request body:
      {"payload": "hex_string"}
    
    Quy trinh xu ly:
      1. Nhan payload hex
      2. Chuyen thanh bytes
      3. Giai ma AES-128-CBC
      4. Kiem tra replay attack
      5. Luu vao database
      6. Tra ve HTTP 200 hoac 403
    
    Tra ve:
      200: {"status": "success", "device": "Xi_01"}
      403: {"status": "error", "reason": "Replay attack..."}
      400: {"status": "error", "message": "Missing payload"}
    """
    # Bat dau do thoi gian
    t_start = time.time()
    
    # Lay JSON tu request
    json_input = request.get_json()
    
    # Kiem tra payload co ton tai khong
    if not json_input or 'payload' not in json_input:
        return jsonify({"status": "error", "message": "Missing payload"}), 400

    try:
        # Lay payload hex tu request
        payload = json_input['payload']
        logging.debug(f"Received payload len={len(payload)} first50={payload[:50]}")
        
        # Chuyen hex string thanh bytes
        raw_data = bytes.fromhex(payload)

        # ----- BUOC 1: GIAI MA AES -----
        t1 = time.time()
        data, error = verify_and_decrypt(raw_data)
        t_decrypt = (time.time() - t1) * 1000  # Chuyen sang ms

        # Neu giai ma that bai
        if error:
            print(f"[!] Loi giai ma: {error}")
            logging.debug(f"Decrypt error: {error}")
            return jsonify({"status": "error", "reason": error}), 403

        # ----- BUOC 2: KIEM TRA REPLAY -----
        t2 = time.time()
        ok, msg = check_seq(data.get('id'), data.get('seq'))
        t_seq = (time.time() - t2) * 1000

        # Neu phat hien replay attack
        if not ok:
            # Ghi log telemetry voi trang thai canh bao
            executor.submit(log_telemetry, data, f"Canh bao: {msg}")
            # Luu benchmark voi status FAIL
            executor.submit(save_benchmark, data.get('id'), t_decrypt, t_seq, 0, 0, "FAIL")
            print(f"[!] {msg}")
            logging.warning(f"REPLAY: device={data.get('id')} seq={data.get('seq')} -> {msg}")
            return jsonify({"status": "error", "reason": msg}), 403

        # ----- BUOC 3: CAP NHAT SEQUENCE VA LUU DATA -----
        t3 = time.time()
        
        # Cap nhat last_seq trong database
        if data.get('seq') is not None:
            update_seq(data.get('id'), data.get('seq'))
        
        # Ghi log telemetry (chay song song de khong block)
        executor.submit(log_telemetry, data, "An toan")
        t_log = (time.time() - t3) * 1000

        # ----- BUOC 4: LUU BENCHMARK -----
        t_total = (time.time() - t_start) * 1000
        print(f"[+] {data.get('id')}: decrypt={t_decrypt:.1f}ms seq={t_seq:.1f}ms log={t_log:.1f}ms total={t_total:.1f}ms")
        executor.submit(save_benchmark, data.get('id'), t_decrypt, t_seq, t_log, t_total, "OK")

        return jsonify({"status": "success", "device": data.get('id')}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# ============================================================
# CHAY SERVER
# ============================================================
if __name__ == "__main__":
    print("=== SERVER IOT XI->Y->SERVER DANG CHAY ===")
    print(f"Database: {DB_NAME}")
    print(f"Key: {NETWORK_KEY}")
    print(f"Port: 5000")
    # host='0.0.0.0': lang nghe tren tat ca interface
    # threaded=True: xu ly nhieu request dong thoi
    app.run(host='0.0.0.0', port=5000, threaded=True)