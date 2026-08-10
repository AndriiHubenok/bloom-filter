import sys
from fp_rate_calculator import (calculate_optimal_bits_hashes,
                                calculate_false_positive_rate,
                                calculate_bits_per_item)
from double_hash import (hash_string, h_a, h_b)

m = 64
k = 2
bits = [0] * m

def h1(s):
    return sum(byte for byte in s.encode("utf-8")) % m

def h2(s):
    return sum(byte * (i + 1) for i, byte in enumerate(s.encode("utf-8"))) % m

out = []
for raw in sys.stdin:
    line = raw.rstrip("\n")
    if not line:
        continue

    parts = line.split(" ")
    cmd = parts[0]
    arg = parts[1:] if len(parts) > 1 else ""

    if cmd == "HASH":

        print(hash_string(arg[0], int(arg[1]), int(arg[2])))

    elif cmd == "HA":

        print(h_a(arg[0]))

    elif cmd == "HB":

        print(h_b(arg[0]))

# sys.stdout.write("\n".join(out) + "\n")
