import numpy as np
from scipy import stats
from .base import LiquidityProfile


class NormalLiquidityProfile(LiquidityProfile):
    """
    Normal distribution liquidity profile, with shape described by one scale parameter: sigma.

    l(t) = (c / (sqrt(2*pi) * sigma)) * np.exp(-t**2 / (2 * sigma**2))
    """
    sigma: float

    def at(self, t: int) -> float:
        return self.c * stats.norm.pdf(t, 0, self.sigma)