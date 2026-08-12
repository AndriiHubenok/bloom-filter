from double_hash import hash_string

MAX_COUNTER = 15

class CountingBloomFilter:

    def __init__(self, m: int, k: int, expected_n=1):
        self.m = m
        self.k = k
        self.counters = [0] * m
        self.n = 0
        self.expected_n = expected_n
        self.load = 0.0

    def save_counters(self, positions):
        for index in positions:
            if self.counters[index] < MAX_COUNTER:
                self.counters[index] += 1

        self.n += 1

    def check_counters(self, positions):
        return all(self.counters[index] > 0 for index in positions)

    def add(self, inp: str):
        hashed_input = hash_string(inp, self.m, self.k)
        self.save_counters(hashed_input)

    def remove(self, inp: str) -> bool:
        hashed_input = hash_string(inp, self.m, self.k)

        if any(self.counters[index] == 0 for index in hashed_input):
            return False

        for index in hashed_input:
            self.counters[index] -= 1

        return True

    def check(self, inp):
        hashed_input = hash_string(inp, self.m, self.k)
        return self.check_counters(hashed_input)

    def count(self, inp):
        hashed_input = hash_string(inp, self.m, self.k)
        return min(self.counters[index] for index in hashed_input)

    def pop_count(self):
        return sum(self.counters)

    def get_bits_string(self):
        return ''.join(str(bit) for bit in self.counters)

    def get_stats(self):
        self.load = round(self.n / self.expected_n, 4)
        return "m={} k={} n={} load={:.4f}".format(self.m, self.k, self.n, self.load)