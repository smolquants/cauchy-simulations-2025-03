import numpy as np
from pydantic import BaseModel, PydanticUserError

from ..profiles.base import LiquidityProfile

class DiscretizedModel(BaseModel):
    """
    Base model for discretizing a continuous liquidity profile.
    """
    t_max: float
    t_spacing: float
    lp: LiquidityProfile

    def ticks(self) -> list[list[float]]:
        """
        List of discrete ticks to add/remove liquidity from.
        """
        raise PydanticUserError("Function not implemented.", code=None)

    def at(self, t: float) -> float:
        """
        Discretized concentrated liquidity value at tick t.
        """
        raise PydanticUserError("Function not implemented.", code=None)

    def cost_y(self, i: int, f: int) -> float:
        """
        Amount of delta(y) in (+) or out (-) of pool to move pool tick
        from i -> f, assuming continuous liquidity profile.

        Raises if relative error is > rtol input.
        """
        def integrand(t: int):
            return (self.at(t) / 2) * np.exp(t/2)

        v = 0
        step_sign = 1 if i < f else -1
        for t in np.arange(start=i, stop=f + self.t_spacing, step=step_sign * self.t_spacing):
            v += (step_sign * self.t_spacing) * integrand(t)

        return v

    def cost_x(self, i: int, f: int) -> float:
        """
        Amount of delta(x) in (+) or out (-) of pool to move pool tick
        from i -> f, assuming continuous liquidity profile.

        Raises if relative error is > rtol input.
        """
        def integrand(t: int):
            return - (self.at(t) / 2) * np.exp(-t/2)

        v = 0
        step_sign = 1 if i < f else -1
        for t in np.arange(start=i, stop=f + self.t_spacing, step=step_sign * self.t_spacing):
            v += (step_sign * self.t_spacing) * integrand(t)

        return v

    def reserves_y(self, t: int) -> float:
        """
        Amount of y reserves housed in pool if at tick value of t.
        Effectively amount of y that can be taken out of pool (-),
        if swapped in infinite x.
        """
        if t < -self.t_max:
            t = -self.t_max
        return -self.cost_y(t, -self.t_max)

    def reserves_x(self, t: int) -> float:
        """
        Amount of x reserves housed in pool if at tick value of t.
        Effectively amount of x that can be taken out of pool (-),
        if swapped in infinite y.
        """
        if t > self.t_max:
            t = self.t_max
        return -self.cost_x(t, self.t_max)
    