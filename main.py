import sys

from bitwise_bloom_filter_operations import union, intersection
from bloom_filter import BloomFilter
from fp_rate_calculator import (calculate_optimal_bits_hashes,
                                calculate_false_positive_rate,
                                calculate_bits_per_item)
from double_hash import (hash_string, h_a, h_b)
from scalable_bloom_filter import ScalableBloomFilter
from cuckoo_filter import CuckooFilter

out = []
bf = BloomFilter(128, 3)
sbf = None
bf_dict = {}
cf = None
for raw in sys.stdin:
    line = raw.rstrip("\n")
    if not line:
        continue

    parts = line.split(" ")
    cmd = parts[0]
    arg = parts[1:] if len(parts) > 1 else ""

    if cmd == "INVALIDATE":
        bf.add(arg[0])

    elif cmd == "CHECK_CACHE":
        print("INVALIDATED (recheck)" if bf.check(arg[0]) else "CACHED (use)")

    elif cmd == "STATS":
        print(bf.get_stats())

# sys.stdout.write("\n".join(out) + "\n")
