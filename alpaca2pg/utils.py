import os

def getenv(name, permissive=False):
    """Fault-intolerant fetcher from env."""
    val = os.getenv(name)
    if val is None and not permissive:
        raise ValueError(f"Missing required input parameter from env: {name}")
    return val.strip()
