from bloom_filter import BloomFilter

def union (a: BloomFilter, b: BloomFilter):
    if a.m != b.m or a.k != b.k:
        raise ValueError("Bloom filters must have the same size and number of hash functions for union operation.")

    result = BloomFilter(a.m, a.k, a.expected_n)
    result.counters = [bit_a | bit_b for bit_a, bit_b in zip(a.counters, b.counters)]
    return result

def intersection (a: BloomFilter, b: BloomFilter):
    if a.m != b.m or a.k != b.k:
        raise ValueError("Bloom filters must have the same size and number of hash functions for intersection operation.")

    result = BloomFilter(a.m, a.k, a.expected_n)
    result.counters = [bit_a & bit_b for bit_a, bit_b in zip(a.counters, b.counters)]
    return result