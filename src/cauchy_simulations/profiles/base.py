import numpy as np
from pydantic import BaseModel, PydanticUserError
from scipy import integrate


class LiquidityProfile(BaseModel):
    """
    Generic model for concentrated liquidity global liquidity density function.
    
    Should require int_{-\infty}^{\infty} l(t)dt = C, where C is a global constant
    when no LPs add or remove funds from pool.

    Assumes continuous liquidity profile and input ticks are in "natural log" form
    such that price p = e ** (t), where t is the tick.
    """
    c: float

    def at(self, t: int) -> float:
        """
        `at` takes a tick value as input and returns the concentrated liquidity value
        in the pool.
        """
        raise PydanticUserError("Function not implemented.", code=None)

    def slip_y(self, t: int) -> float:
        """
        Tick slippage with respect to an infinitesimal amount of y.
        """
        return (2 / self.at(t)) * np.exp(-t/2)

    def slip_x(self, t: int) -> float:
        """
        Tick slippage with respect to an infinitesimal amount of x.
        """
        return - (2 / self.at(t)) * np.exp(t/2)

    def cost_y(self, i: int, f: int, rtol: float = 1e-4) -> float:
        """
        Amount of delta(y) in (+) or out (-) of pool to move pool tick
        from i -> f, assuming continuous liquidity profile.

        Raises if relative error is > rtol input.
        """
        def integrand(t: int):
            return (self.at(t) / 2) * np.exp(t/2)

        (v, er) = integrate.quad(integrand, i, f)
        if er > rtol:
            raise ValueError(f'relative error of {er} exceed rtol of {rtol}.')

        return v

    def cost_x(self, i: int, f: int, rtol: float = 1e-4) -> float:
        """
        Amount of delta(x) in (+) or out (-) of pool to move pool tick
        from i -> f, assuming continuous liquidity profile.

        Raises if relative error is > rtol input.
        """
        def integrand(t: int):
            return - (self.at(t) / 2) * np.exp(-t/2)

        (v, er) = integrate.quad(integrand, i, f)
        if er > rtol:
            raise ValueError(f'relative error of {er} exceed rtol of {rtol}.')

        return v

    def reserves_y(self, t: int, tmax: int, rtol: float = 1e-4) -> float:
        """
        Amount of y reserves housed in pool if at tick value of t.
        Effectively amount of y that can be taken out of pool (-),
        if swapped in infinite x.
        """
        if t < -tmax:
            raise ValueError("Tick max must be largest tick possible on discrete liquidity profile range of [-tmax, tmax].")

        return -self.cost_y(t, -tmax, rtol)

    def reserves_x(self, t: int, tmax: int, rtol: float = 1e-4) -> float:
        """
        Amount of x reserves housed in pool if at tick value of t.
        Effectively amount of x that can be taken out of pool (-),
        if swapped in infinite y.
        """
        if t > tmax:
            raise ValueError("Tick max must be largest tick possible on discrete liquidity profile range of [-tmax, tmax].")

        return -self.cost_x(t, tmax, rtol)