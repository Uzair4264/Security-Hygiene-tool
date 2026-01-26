# src/utils/value_normalizer.py
def normalize_value(val):
    """Return Enum.value if Enum, else return val itself."""
    return val.value if hasattr(val, "value") else val
