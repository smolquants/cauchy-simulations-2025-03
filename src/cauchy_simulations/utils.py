import numpy as np

def from_bps_tick(tb: int) -> float:
    """
    Converts tick in bps form i.e. p = 1.0001 ** (tb)
    to tick in natural log form: p = e ** (t).
    """
    return np.log(1.0001) * tb

def to_bps_tick(t: int) -> float:
    """
    Converts tick in natural log form: p = e ** (t)
    to tick in bps form: p = 1.0001 ** (t).
    """
    return t / np.log(1.0001)