def free_cash_flow (operating_activity,investing_activity):
    return operating_activity+investing_activity
free_cash_flow(500,-500)

def cfo_pat_ratio(operating_profit,net_profit):
    if net_profit == 0:
        return None
    return operating_profit/net_profit

def capex_intensity(investing_activity,sales):
    if sales == 0:
        return None
    return (abs(investing_activity)/sales)*100

def fcf_conversion(fcf,operating_profit):
    if operating_profit == 0:
        return None
    return (abs(fcf)/operating_profit)*100

def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity
):
    cfo_sign = "+" if operating_activity > 0 else "-"
    cfi_sign = "+" if investing_activity > 0 else "-"
    cff_sign = "+" if financing_activity > 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    labels = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "-", "+"): "Shareholder Returns",
        ("+", "+", "-"): "Debt Reduction / Cash Build",
        ("+", "+", "+"): "Expansion / Fund Raising",

        ("-", "-", "-"): "Cash Burn / Debt Repayment",
        ("-", "-", "+"): "Distress",
        ("-", "+", "-"): "Asset Sale / Debt Repayment",
        ("-", "+", "+"): "Distress / Fund Raising",
    }

    return labels[pattern]