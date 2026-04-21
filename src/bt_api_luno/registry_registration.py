from __future__ import annotations

from bt_api_base.balance_utils import simple_balance_handler as _luno_balance_handler
from bt_api_base.registry import ExchangeRegistry

from .exchange_data import LunoExchangeDataSpot
from .feeds.live_luno.spot import LunoRequestDataSpot


def register_luno(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("LUNO___SPOT", LunoRequestDataSpot)
    registry.register_exchange_data("LUNO___SPOT", LunoExchangeDataSpot)
    registry.register_balance_handler("LUNO___SPOT", _luno_balance_handler)


__all__ = ["register_luno"]
