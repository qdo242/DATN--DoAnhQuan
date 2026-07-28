#!/usr/bin/env python3
"""Query database and print summary."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'iot_security.db')

def query_summary():
    if not os.path.exists(DB_PATH):
        print("Database not found. Run init_db.py first.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    
    print("=" * 60)
    print("DATABASE SUMMARY")
    print("=" * 60)
    
    # Devices
    devices = conn.execute("SELECT * FROM devices").fetchall()
    print(f"\nDevices: {len(devices)}")
    for d in devices:
        print(f"  - {d[0]}: {d[1]} ({d[2]})")
    
    # Telemetry
    try:
        tel_count = conn.execute("SELECT COUNT(*) FROM telemetry").fetchone()[0]
        print(f"\nTelemetry records: {tel_count}")
        if tel_count > 0:
            recent = conn.execute("SELECT id, device_id, status, seq FROM telemetry ORDER BY id DESC LIMIT 5").fetchall()
            print("  Recent:")
            for r in recent:
                print(f"    #{r[0]} {r[1]} seq={r[3]} {r[2]}")
    except:
        print("\nTelemetry: table not found")
    
    # Benchmark
    try:
        bench_count = conn.execute("SELECT COUNT(*) FROM benchmark").fetchone()[0]
        print(f"\nBenchmark records: {bench_count}")
        if bench_count > 0:
            stats = conn.execute("""
                SELECT status, COUNT(*), AVG(total_ms) 
                FROM benchmark GROUP BY status
            """).fetchall()
            print("  Stats:")
            for s in stats:
                print(f"    {s[0]}: {s[1]} records, avg {s[2]:.3f}ms")
    except:
        print("\nBenchmark: table not found")
    
    print("=" * 60)
    conn.close()

if __name__ == '__main__':
    query_summary()