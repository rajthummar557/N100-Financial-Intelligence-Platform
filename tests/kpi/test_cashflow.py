from src.analytics.cashflow_kpi import (
    free_cash_flow,
    cfo_pat_ratio,
    capex_intensity,
    fcf_conversion,
    capital_allocation_pattern,
)


def test_free_cash_flow():
    result = free_cash_flow(500, -200)

    assert result == 300


def test_free_cash_flow_negative():
    result = free_cash_flow(100, -250)

    assert result == -150


def test_cfo_pat_ratio():
    result = cfo_pat_ratio(500, 250)

    assert result == 2.0


def test_cfo_pat_ratio_zero_pat():
    result = cfo_pat_ratio(500, 0)

    assert result is None


def test_capex_intensity():
    result = capex_intensity(-200, 1000)

    assert result == 20.0


def test_capex_intensity_zero_sales():
    result = capex_intensity(-200, 0)

    assert result is None


def test_fcf_conversion():
    result = fcf_conversion(300, 400)

    assert result == 75.0


def test_fcf_conversion_zero_operating_profit():
    result = fcf_conversion(300, 0)

    assert result is None


def test_capital_allocation_reinvestor():
    result = capital_allocation_pattern(500, -200, -100)

    assert result == "Reinvestor"


def test_capital_allocation_shareholder_returns():
    result = capital_allocation_pattern(500, -200, 100)

    assert result == "Shareholder Returns"


def test_capital_allocation_distress():
    result = capital_allocation_pattern(-500, -200, 100)

    assert result == "Distress"