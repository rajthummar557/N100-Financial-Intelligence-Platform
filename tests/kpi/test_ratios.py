from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    check_opm_mismatch
)

def test_net_profit_margin():
    assert net_profit_margin(200,1000) == 20.0

def test_net_profit_margin_zero_sales():
    assert net_profit_margin(2000,0) is None

def test_return_on_equity():
    assert return_on_equity(200,100,900)==20.0

def test_return_on_negative_equity():
    assert return_on_equity(200,100,-400) is None

def test_return_on_capital_employed():
    assert return_on_capital_employed(
        202,      # operating_profit
        19,       # depreciation
        100,      # equity_capital
        900,      # reserves
        500       # borrowings
    ) == 12.2

def test_return_on_capital_employed_negative_capital():
    assert return_on_capital_employed(
        202,
        19,
        100,
        -700,
        500
    ) is None

def test_opm_cross_check_mismatch():
    assert check_opm_mismatch(200, 1000, 18) is True

def test_return_on_assets_zero_assets():
    assert return_on_assets(200, 0) is None
