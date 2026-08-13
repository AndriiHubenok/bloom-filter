from double_hash import hash_string

class BloomFilter:

    def __init__(self, m: int, k: int, expected_n=1):
        self.m = m
        self.k = k
        self.bits = [0] * m
        self.n = 0
        self.expected_n = expected_n
        self.checks = 0
        self.rechecks = 0
        self.load = 0.0

    def save_bits(self, positions):
        for index in positions:
            self.bits[index] = 1

        self.n += 1

    def check_bits(self, positions):
        self.checks += 1
        if all(self.bits[index] == 1 for index in positions):
                    self.rechecks += 1
                    return True

        return False

    def add(self, inp: str):
        hashed_input = hash_string(inp, self.m, self.k)
        self.save_bits(hashed_input)

    def check(self, inp):
        hashed_input = hash_string(inp, self.m, self.k)
        return self.check_bits(hashed_input)

    def pop_count(self):
        return sum(self.bits)

    def get_bits_string(self):
        return ''.join(str(bit) for bit in self.bits)

    def get_stats(self):
        return "invalidated={} checks={} rechecks={}".format(self.n, self.checks, self.rechecks)
        # self.load = round(self.n / self.expected_n, 4)
        # return "m={} k={} n={} load={:.4f}".format(self.m, self.k, self.n, self.load)

    def is_full(self) -> bool:
        return self.n >= self.expected_n