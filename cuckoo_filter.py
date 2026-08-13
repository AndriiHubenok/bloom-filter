import random
from double_hash import h_a, h_b

class CuckooFilter:
    def __init__(self, num_buckets: int):
        self.B = num_buckets
        self.buckets = [[0] * 4 for _ in range(num_buckets)]
        self.count = 0
        self.rng = random.Random(0xCAFE)
        self.max_kicks = 500

    def _get_fp(self, s: str) -> int:
        fp = h_b(s) & 0xFF
        if fp == 0:
            fp = 1
        return fp

    def _hash_fp(self, fp: int) -> int:
        return (fp * 0x5bd1e995) & 0xFFFFFFFF

    def _get_indices(self, s: str):
        fp = self._get_fp(s)
        i1 = h_a(s) % self.B
        i2 = (i1 ^ self._hash_fp(fp)) % self.B
        return fp, i1, i2

    def positions(self, s: str) -> str:
        fp, i1, i2 = self._get_indices(s)
        return f"fp={fp} i1={i1} i2={i2}"

    def fp(self, s: str) -> str:
        fp = self._get_fp(s)
        return str(fp)

    def _insert(self, idx: int, fp: int) -> bool:
        for slot in range(4):
            if self.buckets[idx][slot] == 0:
                self.buckets[idx][slot] = fp
                self.count += 1
                return True
        return False

    def add(self, s: str) -> str:
        fp, i1, i2 = self._get_indices(s)

        if self._insert(i1, fp):
            return "OK"
        if self._insert(i2, fp):
            return "OK"

        curr_i = self.rng.choice((i1, i2))
        curr_fp = fp

        for _ in range(self.max_kicks):
            slot = self.rng.randrange(4)
            old_fp = self.buckets[curr_i][slot]
            self.buckets[curr_i][slot] = curr_fp
            curr_fp = old_fp

            curr_i = (curr_i ^ self._hash_fp(curr_fp)) % self.B

            if self._insert(curr_i, curr_fp):
                return "OK"

        return "FULL"

    def check(self, s: str) -> str:
        fp, i1, i2 = self._get_indices(s)
        if fp in self.buckets[i1]:
            return "MAYBE"
        if fp in self.buckets[i2]:
            return "MAYBE"
        return "NO"

    def remove(self, s: str) -> str:
        fp, i1, i2 = self._get_indices(s)

        for slot in range(4):
            if self.buckets[i1][slot] == fp:
                self.buckets[i1][slot] = 0
                self.count -= 1
                return "OK"

        for slot in range(4):
            if self.buckets[i2][slot] == fp:
                self.buckets[i2][slot] = 0
                self.count -= 1
                return "OK"

        return "WAS_ABSENT"

    def get_count(self) -> int:
        return self.count

    def get_load(self) -> str:
        load = self.count / (self.B * 4) if self.B > 0 else 0.0
        return f"{load:.4f}"