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
    def __init__(self) -> None:
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
        return self.rest_url

    def get_wss_url(self) -> str:
        return self.wss_url

    def get_kline_periods(self) -> dict[str, str]:
        return dict(self.kline_periods)

    def get_symbol(self, symbol: str) -> str:
        return symbol.upper()

    def get_rest_path(self, action: str) -> str:
        return self.rest_paths.get(action, "")

    def get_wss_path(self, action: str) -> str:
        return ""

    def get_local_symbol(self, symbol: str) -> str:
        return symbol.lower()

    def is_trading_enabled(self) -> bool:
        return True

    def get_period(self, period: str) -> int:
        return int(self.kline_periods.get(period, "60"))


class LunoExchangeDataSpot(LunoExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"


__all__ = ["LunoExchangeData", "LunoExchangeDataSpot"]
