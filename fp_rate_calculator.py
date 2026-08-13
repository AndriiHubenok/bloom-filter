from math import ceil, log, e, exp


def calculate_optimal_bits_hashes(expected_n: int, target_fp: float):
    m_opt = ceil( -expected_n * log(target_fp, e) / (log(2, e) ** 2))
    k_opt = int(round((m_opt / expected_n) * log(2, e), 0))
    return m_opt, k_opt

def calculate_false_positive_rate(m: int, n: int, k: int) -> float:
    fp = round((1 - exp(-k * n / m)) ** k, 6)
    return fp

def calculate_bits_per_item(target_fp: float) -> float:
    bpi = round(-log(target_fp, e) / (log(2, e) ** 2), 4)
    return bpi