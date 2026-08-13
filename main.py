import sys

from cache import cache
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
hited = 0
misses = 0
bloom_misses = 0
for raw in sys.stdin:
    line = raw.rstrip("\n")
    if not line:
        continue

    parts = line.split(" ")
    cmd = parts[0]
    arg = parts[1:] if len(parts) > 1 else ""

    if cmd == "INIT":
        hited = 0
        misses = 0
        bloom_misses = 0
        bf = BloomFilter(int(arg[0]), float(arg[1]))
        print("OK m={} k={}".format(bf.m, bf.k))

    elif cmd == "PUT_CACHE":
        bf.add(arg[0])
        cache[arg[0]] = arg[1]
        print("OK")

    elif cmd == "GET":
        if bf.check(arg[0]):
            if arg[0] in cache:
                hited += 1
                print("HIT " + cache[arg[0]])
            else:
                print("MISS_BLOOM_FP")
                misses += 1
        else:
            print("BLOOM_MISS")
            bloom_misses += 1

    elif cmd == "INVALIDATE":
        del cache[arg[0]]
        print("OK")

    elif cmd == "STATS":
        print("hits={} misses={} bloom_misses={} bloom_fp={}"
              .format(hited, misses, bloom_misses, misses))

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
