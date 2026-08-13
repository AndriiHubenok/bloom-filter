from double_hash import hash_string
from fp_rate_calculator import calculate_optimal_bits_hashes, calculate_false_positive_rate


class BloomFilter:

    def __init__(self, capacity: int, target_fp: float):
        self.capacity = capacity
        self.target_fp = target_fp
        self.actual_fp = 0.0000
        self.m, self.k = calculate_optimal_bits_hashes(capacity, target_fp)
        self.bits = [0] * self.m
        self.n = 0
        self.checks = 0
        self.rechecks = 0
        self.load = 0.0000
        self.fill = 0.0000

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

    def get_healthy_status(self):
        res = []
        if self.get_load() > 1.0:
            res.append("OVER_CAPACITY")

        elif self.checks >= 10 and self.get_actual_fp() > 2 * self.target_fp:
            res.append("FP_TOO_HIGH")

        elif len(res) == 0:
            res.append("HEALTHY")

        return res


    def get_bits_string(self):
        return ''.join(str(bit) for bit in self.bits)

    def get_load(self):
        self.load = self.n / self.capacity
        return self.load

    def get_fill(self):
        self.fill = sum(self.bits) / len(self.bits)
        return self.fill

    def get_actual_fp(self):
        if self.checks == 0:
            return 0.0000

        self.actual_fp = round(self.rechecks / self.checks, 4)
        return  self.actual_fp

    def get_theoretical_fp(self):
        return calculate_false_positive_rate(self.m, self.n, self.k)

    def get_stats(self):
        return "invalidated={} checks={} rechecks={}".format(self.n, self.checks, self.rechecks)
        # self.load = round(self.n / self.expected_n, 4)
        # return "m={} k={} n={} load={:.4f}".format(self.m, self.k, self.n, self.load)

    def is_full(self) -> bool:
        return self.n >= self.capacity