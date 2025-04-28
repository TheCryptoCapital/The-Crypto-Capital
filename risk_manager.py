from config import CAPITAL, LEVERAGE

def calculate_position_size(symbol: str, entry_price: float, stop_loss: float, risk_usdt: float) -> float:
    """
    Calculates size such that risk_usdt is lost if SL is hit.
    """
    risk_per_unit = abs(entry_price - stop_loss)
    if risk_per_unit == 0:
        return 0
    size = risk_usdt / risk_per_unit
    # apply leverage
    size = size * LEVERAGE
    # round to 2 decimals for cryptos
    return round(size, 2)


