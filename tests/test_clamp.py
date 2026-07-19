from src.utils.clamp import clamp_index


def test_clamp_within_range_unchanged():
    assert clamp_index(2, 10) == 2


def test_clamp_above_range_clamped_to_last():
    assert clamp_index(20, 5) == 4


def test_clamp_negative_clamped_to_zero():
    assert clamp_index(-1, 10) == 0


def test_clamp_empty_count_returns_zero():
    assert clamp_index(5, 0) == 0


def test_clamp_single_item():
    assert clamp_index(0, 1) == 0
