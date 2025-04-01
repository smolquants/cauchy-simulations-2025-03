import numpy as np
from pydantic import BaseModel
from ..profiles.base import LiquidityProfile


class SymmetricModel(BaseModel):
    """
    Symmetric model for deploying concentrated liquidity
    according to a symmetric discretized liquidity profile.

    Adds/remove liquidity by working down the full tick range. Partitions the
    full tick range into N segments each of width 2 * s such that the ith
    segment is between ticks: (s * 2**i, s * 2**(i+1)). Total number
    of segments to cover full tick range: 1 + floor(log(t_max / s) / log(2)).

    Each segment is binned evenly with resolution R_i = 2**(i-r), such that
    within a segment there are always 2**r bins.

    Total ticks to add/remove liquidity would be total number of bins
    across full tick range: 2**r * (1 + floor(log(t_max / s) / log(2))).

    Number of SSTORE calls then grows by log(1/s).
    """
    t_max: float
    s: float
    r: int

    def n(self) -> int:
        """
        Index of widest segment to add/remove liquidity from.
        n = floor(log(t_max / s) / log(2))
        """
        return int(np.floor(np.log(self.t_max / self.s) / np.log(2)))

    def segments(self) -> list[(float, float)]:
        """
        List of segments to add/remove liquidity from.
        """
        _n = self.n()
        return list(self.s * np.array([(2**(_n - i), 2**(_n - i - 1)) for i in range(_n)] + [(1, 0)]))

    def ticks(self) -> list[list[float]]:
        """
        List of ticks to add/remove liquidity from. Within each segment, there are
        2**self.r ticks to add liquidity to.
        """
        _segments = self.segments()
        _r = self.r
        return list(np.array([np.arange(start=i, stop=f, step=(f - i) / 2**_r) for i, f in _segments]).flatten())

    def at(self, t: float, lp: LiquidityProfile) -> float:
        """
        Discretized concentrated liquidity value at tick t.
        
        Chooses continuous liquidity value at the widest tick of the bin that contains t.
        """
        if lp.at(t) != lp.at(-t):
            raise ValueError(f"Liquidity profile is not symmetric at {t}.")

        # ticks are sorted in descending order
        _ticks = self.ticks()
        # should be between 0 and s or > t_max if not in loop otherwise raise error
        if _ticks[-1] >= np.abs(t) >= 0:
            return lp.at(_ticks[-1])
        elif np.abs(t) > _ticks[0]:
            return lp.at(_ticks[0])

        for i in range(len(_ticks) - 1):
            # leftmost is largest in bin
            if _ticks[i] >= np.abs(t) > _ticks[i+1]:
                return lp.at(_ticks[i])

        raise ValueError(f"Tick {t} is not in any bin.")
