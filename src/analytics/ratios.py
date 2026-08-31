def net_profit_margin(net_profit,sales):
    if sales == 0:
        return None
    return (net_profit/sales)*100   



def operating_profit_margin(operating_profit,sales):
    if sales == 0:
        return None
    return (operating_profit/sales)*100


def check_opm_mismatch(operating_profit, sales, source_opm):
    calculated_opm = operating_profit_margin(
        operating_profit,
        sales
    )

    if calculated_opm is None:
        return False

    return abs(calculated_opm - source_opm) > 1

def return_on_equity(net_profit,reserves,equity_capital):
    equity = equity_capital+reserves
    if equity <= 0:
        return None
    return (net_profit/equity)*100

def return_on_capital_employed(oprating_profit,depreciation,equity_capital,reserves,borrowing):
    ebit = oprating_profit-depreciation
    capital = equity_capital+reserves+borrowing
    if capital<=0:
        return None
    return (ebit/capital)*100

def return_on_assets(net_profit,total_assets):
    if total_assets<=0:
        return None
    return (net_profit/total_assets)*100

def debt_to_equity(borrwings,equity_capital,reserves):
    if borrwings==0:
        return 0
    equity = equity_capital+reserves
    if equity<=0:
        return None
    return borrwings/equity
def high_leverage_flag(de_ratio,borad_sector):
    if de_ratio is None:
        return None
    return de_ratio>5 and borad_sector != "Financials"

def interest_coverage(operating_profit, other_income, interest):

    if interest == 0:
        return None

    return (operating_profit + other_income) / interest

def icr_label(interest):
    if interest == 0:
        return "Debt Free"

    return None

def interest_coverage_warning(icr):
    if icr is None:
        return False

    return icr < 1.5
def net_debt(borrowings, investments):
    return borrowings - investments

def asset_turnover(sales, total_assets):

    if total_assets == 0:
        return None

    return sales / total_assets
