def calculate_position_size(symbol, entry_price, stop_loss, risk_usdt):
    # Simple risk model: position size = risk / (entry - stop_loss)
    try:
        risk_per_unit = abs(entry_price - stop_loss)
        if risk_per_unit == 0:
            return 0
        size = risk_usdt / risk_per_unit
        return round(size, 2)
    except Exception as e:
        print(f"Error calculating position size for {symbol}: {e}")
        return 0

