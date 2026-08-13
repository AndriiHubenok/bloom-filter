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

    if cmd == "INIT":
        b = int(parts[1])
        cf = CuckooFilter(b)
        print(f"OK buckets={b} slots={b * 4}")

    elif cmd == "ADD":
        if cf:
            print(cf.add(parts[1]))

    elif cmd == "CHECK":
        if cf:
            print(cf.check(parts[1]))

    elif cmd == "REMOVE":
        if cf:
            print(cf.remove(parts[1]))

    elif cmd == "COUNT":
        if cf:
            print(cf.get_count())

    elif cmd == "LOAD":
        if cf:
            print(cf.get_load())

    elif cmd == "FP":
        if cf:
            print(cf.fp(parts[1]))

    elif cmd == "POSITIONS":
        if cf:
            print(cf.positions(parts[1]))

# sys.stdout.write("\n".join(out) + "\n")
