import sys

from bitwise_bloom_filter_operations import union, intersection
from bloom_filter import BloomFilter
from fp_rate_calculator import (calculate_optimal_bits_hashes,
                                calculate_false_positive_rate,
                                calculate_bits_per_item)
from double_hash import (hash_string, h_a, h_b)

out = []
bf_dict = {}
for raw in sys.stdin:
    line = raw.rstrip("\n")
    if not line:
        continue

    parts = line.split(" ")
    cmd = parts[0]
    arg = parts[1:] if len(parts) > 1 else ""

    if cmd == "INIT":

        # m, k = calculate_optimal_bits_hashes(float(arg[2]), int(arg[1]))
        bf = BloomFilter(int(arg[1]), int(arg[2]))
        bf_dict[arg[0]] = bf

        print("OK")

    elif cmd == "ADD":

        bf_dict[arg[0]].add(arg[1])
        print("OK")

    elif cmd == "CHECK":

        print("MAYBE" if bf_dict[arg[0]].check(arg[1]) else "NO")

    elif cmd == "UNION":

        bf_dict[arg[0]] = union(bf_dict[arg[1]], bf_dict[arg[2]])
        print("OK")

    elif cmd == "INTERSECT":

        bf_dict[arg[0]] = intersection(bf_dict[arg[1]], bf_dict[arg[2]])
        print("OK")

    elif cmd == "POPCOUNT":

        print(bf_dict[arg[0]].pop_count())

    elif cmd == "BITS":

        print(bf_dict[arg[0]].get_bits_string())

# sys.stdout.write("\n".join(out) + "\n")
