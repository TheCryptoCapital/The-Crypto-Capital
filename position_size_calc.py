# position_size_calc.py
def calculate_position_size(capital, entry_price, stop_loss, risk_percent):
    risk_amount = capital * risk_percent
    risk_per_unit = abs(entry_price - stop_loss)
    return risk_amount / risk_per_unit if risk_per_unit else 0

