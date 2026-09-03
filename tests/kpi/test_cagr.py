from src.analytics.cagr import calculate_cagr


def test_normal_cagr():
    result, flag = calculate_cagr(100, 121, 2, 2)

    assert round(result, 2) == 10.0
    assert flag is None


def test_zero_base():
    result, flag = calculate_cagr(0, 100, 5, 5)

    assert result is None
    assert flag == "ZERO_BASE"


def test_insufficient_data():
    result, flag = calculate_cagr(100, 150, 5, 3)

    assert result is None
    assert flag == "INSUFFICIENT"


def test_decline_to_loss():
    result, flag = calculate_cagr(100, -50, 5, 5)

    assert result is None
    assert flag == "DECLINE_TO_LOSS"


def test_turnaround(): 
    result, flag = calculate_cagr(-100, 50, 5, 5)

    assert result is None
    assert flag == "TURNAROUND"


def test_both_negative():
    result, flag = calculate_cagr(-100, -50, 5, 5)

    assert result is None
    assert flag == "BOTH_NEGATIVE"