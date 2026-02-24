def format_currency(value: float, currency: str) -> str:
    """Simple helper that formats a number with 2 decimals and the currency code."""
    return f"{value:,.2f} {currency}"