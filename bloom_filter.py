from double_hash import hash_string

class BloomFilter:

    def __init__(self, m: int, k: int, expected_n: int):
        self.m = m
        self.k = k
        self.bits = [0] * m
        self.n = 0
        self.expected_n = expected_n
        self.load = 0.0

    def save_bits(self, s):
        for i in range(self.k):
            index = sum(byte * (i + 1) for byte in s.encode("utf-8")) % self.m
            self.bits[index] = 1
        self.n += 1

    def check_bits(self, s):
        for i in range(self.k):
            index = sum(byte * (i + 1) for byte in s.encode("utf-8")) % self.m
            if self.bits[index] != 1:
                return False
        return True

    def add(self, inp: str):
        hashed_input = hash_string(inp, self.m, self.k)
        self.save_bits(hashed_input)

    def check(self, inp):
        hashed_input = hash_string(inp, self.m, self.k)
        return self.check_bits(hashed_input)

    def get_stats(self):
        self.load = round(self.n / self.expected_n, 4)
        return "m={} k={} n={} load={:.4f}".format(self.m, self.k, self.n, self.load)