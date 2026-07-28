# Benchmark Results

## AES vs XOR Performance

| Payload | AES Enc | AES Dec | XOR Enc | XOR Dec | Ratio |
|---------|---------|---------|---------|---------|-------|
| 146B    | 6.65us  | 6.73us  | 8.85us  | 8.93us  | 0.8x  |
| 147B    | 6.55us  | 7.25us  | 9.55us  | 9.24us  | 0.7x  |
| 147B    | 6.98us  | 6.50us  | 8.93us  | 8.82us  | 0.8x  |
| 146B    | 6.78us  | 6.48us  | 8.98us  | 8.95us  | 0.7x  |
| 146B    | 6.81us  | 6.66us  | 9.08us  | 8.86us  | 0.8x  |

**Average**: AES ~13.4us, XOR ~17.9us

## Server Benchmark (from DB)

| Metric | Value |
|--------|-------|
| Decrypt | 0.049ms |
| Seq Check | 3.634ms |
| DB Write | 6.909ms |
| Total | 10.455ms |
| OK | 15 |
| FAIL (replay) | 4 |

## Key Findings

- AES is faster than XOR on modern CPUs
- XOR is simpler but NOT secure
- AES recommended for production IoT