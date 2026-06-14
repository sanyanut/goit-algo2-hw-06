import json
import time
from datasketch import HyperLogLog


def load_data(file_path: str) -> list:
    ips = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                ip = data.get("remote_addr")
                if ip:
                    ips.append(ip)
            except json.JSONDecodeError:
                continue
    return ips


def exact_count(ips: list):
    start_time = time.time()
    unique_ips = set(ips)
    count = len(unique_ips)
    end_time = time.time()
    return count, end_time - start_time


def hll_count(ips: list):
    start_time = time.time()
    hll = HyperLogLog(p=14)
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    count = hll.count()
    end_time = time.time()
    return count, end_time - start_time


if __name__ == "__main__":
    file = "lms-stage-access.log"

    print("Loading data from log file...")
    ips_data = load_data(file)
    print(f"Loaded {len(ips_data)} records. Starting counting...\n")

    exact_res, exact_time = exact_count(ips_data)
    hll_res, hll_time = hll_count(ips_data)

    print("Comparison results:")
    print(f"{'':<25} {'Exact count':<20} {'HyperLogLog':<15}")
    print(f"{'Unique elements':<25} {float(exact_res):<20.1f} {float(hll_res):<15.1f}")
    print(f"{'Execution time (sec.)':<25} {exact_time:<20.5f} {hll_time:<15.5f}")