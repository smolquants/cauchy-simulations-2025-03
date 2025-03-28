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
