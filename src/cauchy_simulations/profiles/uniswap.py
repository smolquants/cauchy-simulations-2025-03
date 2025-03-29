from .base import LiquidityProfile


class UniswapLiquidityProfile(LiquidityProfile):
    """
    Liquidity profile for a Uniswap v2 AMM.
    """
    def at(self, t: int) -> float:
        return self.c
