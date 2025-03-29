import numpy as np
from scipy import stats
from .base import LiquidityProfile


class CauchyLiquidityProfile(LiquidityProfile):
    """
    Cauchy distribution liquidity profile, with shape described by one scale parameter: gamma.

    l(t) = (c / (pi * gamma)) * (1 / (1 + (t / gamma) ** 2))
    """
    gamma: float

    def at(self, t: int) -> float:
        return self.c * stats.cauchy.pdf(t, 0, self.gamma)


class ModifiedCauchyLiquidityProfile(CauchyLiquidityProfile):
    """
    Modified Cauchy distribution liquidity profile, with shape described by
    one scale parameter: gamma, and a background constant liquidity set as the
    value of Cauchy distribution at a location parameter: peg.

    l(t) = l_cauchy(t) + l_cauchy(peg)
    """
    peg: float  # tick at which modified liquidity profile is calibrated

    def at(self, t: int) -> float:
        return super().at(t) + super().at(self.peg)


class VariableCauchyLiquidityProfile(CauchyLiquidityProfile):
    """
    Variable Cauchy distribution liquidity profile, with shape described by
    one scale parameter: gamma, that varies with tick.

    gamma(t) = gamma * sqrt(1 + (t/gamma)^2)

    such that for tick near 0 acts as a constant, and tick -> +/- inf acts
    proportional to t so (t/gamma) -> constant.

    Usual normalization constant ignored.
    """
    def at(self, t: int) -> float:
        t_scaled = t / self.gamma
        return self.c * (1 / (1 + (t_scaled / np.sqrt(1 + t_scaled**2))**2))
