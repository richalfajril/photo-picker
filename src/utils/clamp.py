"""Numeric clamping helpers."""


def clamp_index(index: int, count: int) -> int:
    """Clamp an index into the valid range [0, count-1]. Returns 0 when count <= 0."""
    if count <= 0:
        return 0
    return max(0, min(index, count - 1))
