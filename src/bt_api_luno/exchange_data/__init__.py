"""Module-level docstring."""
from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


_REST_PATHS = {
    "ticker": "/ticker",
    "orderbook": "/orderbook",
    "trades": "/trades",
    "candles": "/candles",
    "markets": "/markets",
    "balance": "/balance",
    "postorder": "/postorder",
    "stoporder": "/stoporder",
}


class LunoExchangeData(ExchangeData):
    """Class LunoExchangeData"""
    def __init__(self) -> None:
        """__init__ method"""
        super().__init__()
        self.exchange_name = "LUNO___SPOT"
        self.rest_url = "https://api.luno.com/api/1"
        self.rest_exchange_url = self.rest_url
        self.wss_url = "wss://api.luno.com/api/1"
        self.rest_paths = dict(_REST_PATHS)
        self.kline_periods = {
            "1m": "1",
            "5m": "5",
            "15m": "15",
            "30m": "30",
            "1h": "60",
            "4h": "240",
            "1d": "1440",
        }

    def get_rest_url(self) -> str:
        """get_rest_url method"""
        return self.rest_url

    def get_wss_url(self) -> str:
        """get_wss_url method"""
        return self.wss_url

    def get_kline_periods(self) -> dict[str, str]:
        """get_kline_periods method"""
        return dict(self.kline_periods)

    def get_symbol(self, symbol: str) -> str:
        """get_symbol method"""
        return symbol.upper()

    def get_rest_path(self, action: str) -> str:
        """get_rest_path method"""
        return self.rest_paths.get(action, "")

    def get_wss_path(self, action: str) -> str:
        """get_wss_path method"""
        return ""

    def get_local_symbol(self, symbol: str) -> str:
        """get_local_symbol method"""
        return symbol.lower()

    def is_trading_enabled(self) -> bool:
        """is_trading_enabled method"""
        return True

    def get_period(self, period: str) -> int:
        """get_period method"""
        return int(self.kline_periods.get(period, "60"))


class LunoExchangeDataSpot(LunoExchangeData):
    """Class LunoExchangeDataSpot"""
    def __init__(self) -> None:
        """__init__ method"""
        super().__init__()
        self.asset_type = "SPOT"


__all__ = ["LunoExchangeData", "LunoExchangeDataSpot"]
