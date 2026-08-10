def hash_string(s: str, m: int, k: int) -> str:
    base_a = h_a(s)
    base_b = h_b(s)
    positions = [(base_a + i * base_b) % m for i in range(k)]
    return ",".join(str(pos) for pos in positions)

def h_a(s: str) -> int:
    """Calculate base hash h_a masked to 32 bits."""
    return sum(byte * (i + 1) for i, byte in enumerate(s.encode("utf-8"))) & 0xFFFFFFFF

def h_b(s: str) -> int:
    """Calculate base hash h_b masked to 32 bits."""
    return sum(byte ^ (i + 1) for i, byte in enumerate(s.encode("utf-8"))) & 0xFFFFFFFF