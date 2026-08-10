import sys

# A basic Bloom filter with two hand-computable hashes.
# Parameters fixed: m = 64 bits, k = 2 hash functions.

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

    parts = line.split(" ", 1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    if cmd == "ADD":

        h_1 = h1(arg)
        h_2 = h2(arg)
        bits[h_1] = 1
        bits[h_2] = 1
        print("OK")

    elif cmd == "CHECK":

        h_1 = h1(arg)
        h_2 = h2(arg)

        if bits[h_1] == 1 and bits[h_2] == 1:
            print("MAYBE")
        else:
            print("NO")

    elif cmd == "BITS":

        print("".join(str(bit) for bit in bits))

# sys.stdout.write("\n".join(out) + "\n")
