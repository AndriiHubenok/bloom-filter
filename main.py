import sys

from bitwise_bloom_filter_operations import union, intersection
from bloom_filter import BloomFilter
from fp_rate_calculator import (calculate_optimal_bits_hashes,
                                calculate_false_positive_rate,
                                calculate_bits_per_item)
from double_hash import (hash_string, h_a, h_b)
from scalable_bloom_filter import ScalableBloomFilter

out = []
sbf = None
bf_dict = {}
for raw in sys.stdin:
    line = raw.rstrip("\n")
    if not line:
        continue

    parts = line.split(" ")
    cmd = parts[0]
    arg = parts[1:] if len(parts) > 1 else ""

    if cmd == "INIT":

        sbf = ScalableBloomFilter(int(arg[0]), float(arg[1]))
        print("OK m={} k={}".format(sbf.filters[-1].m, sbf.filters[-1].k))

    elif cmd == "ADD":

        sbf.add(arg[0])
        print("OK")

    elif cmd == "CHECK":

        print("MAYBE" if sbf.check(arg[0]) else "NO")

    elif cmd == "FILTERS":

        print(len(sbf.filters))

    elif cmd == "TOTAL":

        print(sbf.total_n)

# sys.stdout.write("\n".join(out) + "\n")
