"""
Compare exact vs. HyperLogLog unique-count performance on IP logs.
"""

import time
import json
import ipaddress
from datasketch import HyperLogLog
from tabulate import tabulate

LOG_FILE      = 'lms-stage-access.log'
HLL_PRECISION = 14  # 2^14 registers → ~1% relative error

def is_valid_ip(s: str) -> bool:
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False

def load_ips(path: str) -> list:
    ips = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            ip = record.get("remote_addr", "")
            if is_valid_ip(ip):
                ips.append(ip)
    return ips

def exact_count(ips: list) -> int:
    return len(set(ips))

def hll_count(ips: list, p: int = HLL_PRECISION) -> float:
    """
    Return the approximate unique count using HyperLogLog(p)
    """
    hll = HyperLogLog(p)
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    return float(len(hll))

def main():
    # 1) Load IP addresses
    ips = load_ips(LOG_FILE)

    # 2) Exact unique count timing
    t0 = time.time()
    exact = exact_count(ips)
    t_exact = time.time() - t0

    # 3) HyperLogLog approximate count timing
    t0 = time.time()
    approx = hll_count(ips)
    t_hll = time.time() - t0

    # 4) Print comparison table
    table = [
        ["Unique elements", exact, f"{approx:.1f}"],
        ["Time (s)",        f"{t_exact:.4f}", f"{t_hll:.4f}"]
    ]
    headers = ["Metric", "Exact count", "HyperLogLog"]
    print("\nResults comparison:\n")
    print(tabulate(
        table,
        headers=headers,
        tablefmt="github",
        stralign="center",
        numalign="center"
    ), "\n")

if __name__ == '__main__':
    main()
