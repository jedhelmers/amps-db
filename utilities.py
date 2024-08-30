def trim_trailing_zeros(value: str) -> str:
    """
    Trims trailing zeros and unnecessary decimal points from a string representation of a number.
    
    Args:
        value (str): The string representation of a number.
    
    Returns:
        str: The trimmed string without unnecessary trailing zeros.
    """
    if '.' in value:
        value = value.rstrip('0').rstrip('.')
    return value

def convert_resistor_value(value: int) -> str:
    """
    Converts resistor integer values into metric notation and trims trailing zeros.
    
    Args:
        value (int): The resistor value in ohms.
    
    Returns:
        str: The formatted resistor value with metric notation.
    """
    if value >= 1_000_000:
        return trim_trailing_zeros(f"{value / 1_000_000:.2f}") + "MΩ"
    elif value >= 1_000:
        return trim_trailing_zeros(f"{value / 1_000:.2f}") + "kΩ"
    else:
        return f"{value}Ω"

def convert_capacitor_value(value: float) -> str:
    """
    Converts capacitor values from microfarads to metric notation and trims trailing zeros.
    
    Args:
        value (float): The capacitor value in microfarads.
    
    Returns:
        str: The formatted capacitor value with metric notation.
    """
    if value >= 1_000_000:
        return trim_trailing_zeros(f"{value / 1_000_000:.2f}") + "F"  # Farads
    elif value >= 1_000:
        return trim_trailing_zeros(f"{value / 1_000:.2f}") + "mF"  # Millifarads
    elif value >= 1:
        return trim_trailing_zeros(f"{value:.2f}") + "µF"  # Microfarads
    elif value >= 0.001:
        return trim_trailing_zeros(f"{value * 1_000:.2f}") + "nF"  # Nanofarads
    else:
        return trim_trailing_zeros(f"{value * 1_000_000:.2f}") + "pF"  # Picofarads

def convert_current_value(value: float) -> str:
    """
    Converts capacitor values from microfarads to metric notation and trims trailing zeros.
    
    Args:
        value (float): The capacitor value in microfarads.
    
    Returns:
        str: The formatted capacitor value with metric notation.
    """
    if value >= 1_000_000:
        return trim_trailing_zeros(f"{value / 1_000_000:.2f}") + "A"  # Farads
    elif value >= 1_000:
        return trim_trailing_zeros(f"{value / 1_000:.2f}") + "mA"  # Millifarads
    elif value >= 1:
        return trim_trailing_zeros(f"{value:.2f}") + "µA"  # Microfarads
    elif value >= 0.001:
        return trim_trailing_zeros(f"{value * 1_000:.2f}") + "nA"  # Nanofarads
    else:
        # return trim_trailing_zeros(f"{value * 1_000_000:.2f}") + "pA"  # Picofarads
        return f"{value * 1:.2f}A"

def to_csv(arr):
    output = []

    if not arr:
        return []

    # Load headers
    headers = ','.join(arr[0].keys())

    output.append(headers)

    for row in arr:
        output.append(','.join([
            str(v)
            for v in row.values()
        ]))

    return output