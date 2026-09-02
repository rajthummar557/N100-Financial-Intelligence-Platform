from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    check_opm_mismatch,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage,
    icr_label,
    interest_coverage_warning,
    net_debt,
    asset_turnover
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



#day 9

def test_debt_to_equity():
    assert debt_to_equity(500, 100, 900) == 0.5


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 900) == 0


def test_high_leverage_flag():
    assert high_leverage_flag(6, "Industrials") is True


def test_high_leverage_financials():
    assert high_leverage_flag(6, "Financials") is False


def test_interest_coverage_zero_interest():
    assert interest_coverage(200, 20, 0) is None


def test_icr_label_debt_free():
    assert icr_label(0) == "Debt Free"


def test_interest_coverage_warning():
    assert interest_coverage_warning(1.2) is True


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None

def test_net_debt():
    assert net_debt(500, 200) == 300


# day 10

import pandas as pd

from src.analytics.cagr import calculate_cagr, matric_cagr


def test_normal_cagr():
    result, flag = calculate_cagr(100, 121, 2, 2)

    assert round(result, 2) == 10.0
    assert flag is None


def test_zero_base():
    result, flag = calculate_cagr(0, 100, 5, 5)

    assert result is None
    assert flag == "ZERO_BASE"


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


def test_invalid_years():
    result, flag = calculate_cagr(100, 200, 0)

    assert result is None
    assert flag == "INSUFFICIENT"


def test_matric_cagr_exact_start():
    df = pd.DataFrame({
        "year": [
            "2019-03",
            "2020-03",
            "2021-03",
            "2022-03",
            "2023-03",
            "2024-03"
        ],
        "sales": [100, 110, 120, 130, 140, 150]
    })

    cagr, flag, start, end = matric_cagr(df, "sales", 5)

    assert flag is None
    assert start == "2019-03"
    assert end == "2024-03"


def test_matric_cagr_nearest_earlier():
    df = pd.DataFrame({
        "year": [
            "2017-03",
            "2018-03",
            "2020-03",
            "2021-03",
            "2022-03",
            "2023-03",
            "2024-03"
        ],
        "sales": [100, 110, 120, 130, 140, 150, 160]
    })

    cagr, flag, start, end = matric_cagr(df, "sales", 5)

    assert flag is None
    assert start == "2018-03"
    assert end == "2024-03"


def test_matric_cagr_insufficient():
    df = pd.DataFrame({
        "year": ["2023-03", "2024-03"],
        "sales": [100, 150]
    })

    cagr, flag, start, end = matric_cagr(df, "sales", 5)

    assert cagr is None
    assert flag == "INSUFFICIENT"


def test_matric_cagr_ignores_parse_error():
    df = pd.DataFrame({
        "year": [
            "2022-03",
            "2023-03",
            "2024-03",
            "PARSE_ERROR"
        ],
        "sales": [100, 110, 120, 500]
    })

    cagr, flag, start, end = matric_cagr(df, "sales", 2)

    assert flag is None
    assert start == "2022-03"
    assert end == "2024-03"