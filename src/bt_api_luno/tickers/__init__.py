from __future__ import annotations

from typing import Any

from bt_api_base.containers.tickers.ticker import TickerData


class LunoRequestTickerData(TickerData):
    def __init__(
        self,
        ticker_info: Any,
        symbol_name: str | None = None,
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "LUNO"
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_symbol_name: str | None = None
        self.timestamp: int | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.bid_volume: float | None = None
        self.ask_volume: float | None = None
        self.last_volume: float | None = None
        self.volume_24h: float | None = None
        self.high_24h: float | None = None
        self.has_been_init_data = False
        self.low_24h: float | None = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> LunoRequestTickerData:
        return cls(
            data, symbol_name=data.get("pair"), asset_type="SPOT", has_been_json_encoded=True,
        )

    def init_data(self) -> LunoRequestTickerData:
        if self.has_been_init_data:
            return self

        data = self.ticker_info if isinstance(self.ticker_info, dict) else {}
        self.ticker_symbol_name = data.get("pair")
        if self.symbol_name is None:
            self.symbol_name = self.ticker_symbol_name

        self.last_price = self._as_float(data.get("last_trade"))
        self.bid_price = self._as_float(data.get("bid"))
        self.ask_price = self._as_float(data.get("ask"))
        self.bid_volume = self._as_float(data.get("best_bid_quantity"))
        self.ask_volume = self._as_float(data.get("best_ask_quantity"))
        self.last_volume = self._as_float(data.get("last_trade_volume"))
        self.volume_24h = self._as_float(data.get("rolling_24_hour_volume", data.get("volume_24h")))
        self.high_24h = self._as_float(data.get("rolling_24_hour_high"))
        self.low_24h = self._as_float(data.get("rolling_24_hour_low"))
        self.timestamp = self._as_int(data.get("timestamp"))
        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        raise NotImplementedError

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_local_update_time(self) -> float:
        if self.timestamp is None:
            return 0.0
        return float(self.timestamp)

    def get_symbol_name(self) -> str:
        return self.symbol_name or ""

    def get_ticker_symbol_name(self) -> str | None:
        return self.ticker_symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_server_time(self) -> float | None:
        if self.timestamp is None:
            return None
        return float(self.timestamp)

    def get_bid_price(self) -> float | None:
        return self.bid_price

    def get_ask_price(self) -> float | None:
        return self.ask_price

    def get_bid_volume(self) -> float | None:
        return self.bid_volume

    def get_ask_volume(self) -> float | None:
        return self.ask_volume

    def get_last_price(self) -> float | None:
        return self.last_price

    def get_last_volume(self) -> float | None:
        return self.last_volume

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return object.__repr__(self)

    @staticmethod
    def _as_float(value: Any) -> float | None:
        if value in (None, ""):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _as_int(value: Any) -> int | None:
        if value in (None, ""):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None


__all__ = ["LunoRequestTickerData"]
