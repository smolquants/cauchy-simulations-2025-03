import numpy as np
from scipy import stats
from pydantic import PydanticUserError
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
    a scale parameter: gamma, that can vary with tick.
    """
    def _gamma(self, t: int) -> float:
        """
        Gamma as a function of tick.
        """
        raise PydanticUserError("Function not implemented.", code=None)

    def at(self, t: int) -> float:
        return self.c * stats.cauchy.pdf(t, 0, self._gamma(t))
    

class SquaredVariableCauchyLiquidityProfile(VariableCauchyLiquidityProfile):
    """
    Variable Cauchy distribution liquidity profile, with shape described by
    a scale parameter: gamma, that varies with tick and
    acceleration parameter: a, that describes the speed of transition
    of gamma from constant to proportional to t^2.

    gamma(t) = gamma * (1 + (t/(a * gamma))^2)

    such that for tick near 0 acts as a constant, and tick -> +/- inf acts
    proportional to t^2 so liquidity density profile -> constant.
    """
    a: float

    def _gamma(self, t: int) -> float:
        return self.gamma * (1 + (t/(self.a * self.gamma))**2)
