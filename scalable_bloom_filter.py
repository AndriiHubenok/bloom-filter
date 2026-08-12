from double_hash import hash_string
from bloom_filter import BloomFilter
from fp_rate_calculator import calculate_optimal_bits_hashes

class ScalableBloomFilter:

    def __init__(self, expected_n: int, fp: float):
        self.current_expected_n = expected_n
        self.current_fp = fp
        m, k = calculate_optimal_bits_hashes(fp, expected_n)
        self.filters = [BloomFilter(m, k, expected_n)]
        self.total_n = 0

    def add(self, inp: str):
        if self.filters[-1].is_full():
            self.current_expected_n *= 2
            self.current_fp *= 0.5
            m, k = calculate_optimal_bits_hashes(self.current_fp, self.current_expected_n)
            self.filters.append(BloomFilter(m, k, self.current_expected_n))

        self.filters[-1].add(inp)
        self.total_n += 1

    def check(self, inp):
        for f in reversed(self.filters):
            if f.check(inp):
                return True

        return False