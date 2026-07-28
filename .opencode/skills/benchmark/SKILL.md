---
name: benchmark
description: Use when the user wants to run crypto benchmarks or performance tests. Trigger on "benchmark", "performance", "test speed", "aes vs xor", "so sanh", "toc do", "hieu nang". Runs AES-128-CBC vs XOR comparison with real data.
---

# Run Benchmark

## Quick Start

```cmd
cd C:\ĐATN\server
python benchmark_crypto.py
```

## What It Does

1. Read real AES data from SQLite database (19 records)
2. Generate 5 JSON payloads (145-147B) matching Wokwi format
3. Run 2000 iterations each for AES and XOR
4. Compare encrypt/decrypt times
5. Generate chart: `docs/images/benchmark_crypto.png`

## Output

| Output | Location |
|--------|----------|
| Console | Performance table (us) |
| Chart | `docs/images/benchmark_crypto.png` |

## Real Database Data (19 records)

| ID | Device | Decrypt | Seq | Log | Total | Status |
|----|--------|---------|-----|-----|-------|--------|
| 1 | Xi_01 | 0.061 | 1.800 | 2.937 | 4.990 | OK |
| 2 | Xi_01 | 0.036 | 1.356 | 0.000 | 0.000 | FAIL |
| 3 | Xi_01 | 0.036 | 0.780 | 0.000 | 0.000 | FAIL |
| 4 | Xi_01 | 0.037 | 22.718 | 48.689 | 71.593 | OK |
| 5 | Xi_01 | 0.049 | 1.457 | 0.000 | 0.000 | FAIL |
| 6 | Xi_01 | 0.037 | 26.766 | 33.422 | 60.398 | OK |
| 7 | Xi_01 | 0.040 | 1.560 | 0.000 | 0.000 | FAIL |
| 8 | Xi_02 | 0.068 | 1.025 | 4.161 | 5.481 | OK |
| 9 | Xi_01 | 0.066 | 1.741 | 5.574 | 7.586 | OK |
| 10 | Xi_01 | 0.048 | 0.613 | 2.268 | 3.091 | OK |
| 11 | Xi_02 | 0.047 | 1.513 | 3.025 | 4.742 | OK |
| 12 | Xi_01 | 0.051 | 0.526 | 2.369 | 3.113 | OK |
| 13 | Xi_02 | 0.048 | 1.559 | 2.272 | 4.048 | OK |
| 14 | Xi_01 | 0.051 | 0.495 | 2.704 | 3.412 | OK |
| 15 | Xi_02 | 0.053 | 1.801 | 14.299 | 16.372 | OK |
| 16 | Xi_01 | 0.052 | 0.512 | 2.249 | 2.980 | OK |
| 17 | Xi_02 | 0.048 | 1.599 | 2.430 | 4.241 | OK |
| 18 | Xi_01 | 0.053 | 0.659 | 2.529 | 3.456 | OK |
| 19 | Xi_02 | 0.049 | 0.571 | 2.342 | 3.135 | OK |

## Real Statistics

| Metric | Value |
|--------|-------|
| Total records | 19 |
| Success (OK) | 15 (78.9%) |
| Replay blocked (FAIL) | 4 (21.1%) |
| Avg Decrypt | 0.049ms |
| Avg Seq Check | 3.634ms |
| Avg DB Write | 6.909ms |
| Avg Total | 10.455ms |

## AES vs XOR Benchmark

| Payload | AES Enc | AES Dec | XOR Enc | XOR Dec | Ratio |
|---------|---------|---------|---------|---------|-------|
| 146B | 6.65us | 6.73us | 8.85us | 8.93us | 0.8x |
| 147B | 6.55us | 7.25us | 9.55us | 9.24us | 0.7x |
| 147B | 6.98us | 6.50us | 8.93us | 8.82us | 0.8x |
| 146B | 6.78us | 6.48us | 8.98us | 8.95us | 0.7x |
| 146B | 6.81us | 6.66us | 9.08us | 8.86us | 0.8x |

**Average**: AES ~13.4us, XOR ~17.9us

## Key Findings

- AES is faster than XOR on modern CPUs
- XOR is simpler but NOT secure
- AES recommended for production IoT
- ESP32 HW accelerator makes AES even faster (~17us)

## Benchmark Code Structure

```python
# 1. Read DB data
db_path = '../iot_security.db'
conn = sqlite3.connect(db_path)
rows = conn.execute("SELECT * FROM benchmark").fetchall()

# 2. Generate Wokwi-like JSON payloads
def make_wokwi_payload(seq):
    return {
        "id": f"Xi_{random.randint(1,2):02d}",
        "t": round(random.uniform(25, 31), 1),
        # ... more fields
    }

# 3. Benchmark functions
def bench(func, data, iters=2000):
    times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        func(data)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1_000_000)
    return statistics.mean(times)

# 4. Run benchmarks
for size in PAYLOAD_SIZES:
    pt = make_wokwi_payload(seq)
    aes_time = bench(aes_encrypt, pt)
    xor_time = bench(xor_encrypt, pt)

# 5. Generate chart
plt.savefig('docs/images/benchmark_crypto.png')
```

## Related Files

| File | Purpose |
|------|---------|
| `benchmark_crypto.py` | Main benchmark script |
| `xor_cipher.py` | XOR implementation |
| `docs/images/benchmark_crypto.png` | Generated chart |