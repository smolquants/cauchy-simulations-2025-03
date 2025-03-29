from .base import LiquidityProfile


class CurveLiquidityProfile(LiquidityProfile):
    """
    Liquidity profile for a Curve AMM.
    """
    A: float

    def at(self, t: int) -> float:
        """
        Returns liquidity at current tick for Curve as dy/dsqrt(P).
        """
        return 0
