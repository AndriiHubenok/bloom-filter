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
bf = None
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
        bf = BloomFilter(int(arg[0]), float(arg[1]))
        print("OK m={} k={}".format(bf.m, bf.k))

    elif cmd == "ADD":
        bf.add(arg[0])
        print("OK")

    elif cmd == "PROBE":
        print("MAYBE" if bf.check(arg[0]) else "OK")

    elif cmd == "LOAD":
        print('{:.4f}'.format(bf.get_load()))

    elif cmd == "FILL":
        print('{:.4f}'.format(bf.get_fill()))

    elif cmd == "ACTUAL_FP":
        print('{:.4f}'.format(bf.get_actual_fp()))

    elif cmd == "THEORETICAL_FP":
        print('{:.4f}'.format(bf.get_theoretical_fp()))

    elif cmd == "HEALTHY":
        res = bf.get_healthy_status()
        if res[0] == "HEALTHY":
            print(res[0])
        else:
            print("DEGRADED " + ", ".join(res))

# sys.stdout.write("\n".join(out) + "\n")
