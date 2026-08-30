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
