"""
Cauchy Simulations package for analyzing liquidity profiles and slippage in the automated market maker.
"""

__version__ = "0.1.0"

from .profiles.base import LiquidityProfile
from .profiles.cauchy import CauchyLiquidityProfile, ModifiedCauchyLiquidityProfile
from .utils import from_bps_tick, to_bps_tick

__all__ = [
    "LiquidityProfile",
    "CauchyLiquidityProfile", 
    "ModifiedCauchyLiquidityProfile",
    "from_bps_tick",
    "to_bps_tick"
]