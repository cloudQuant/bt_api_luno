from __future__ import annotations

import time
from typing import Any

from bt_api_base.feeds.capability import Capability

from bt_api_luno.feeds.live_luno.request_base import LunoRequestData


class LunoRequestDataSpot(LunoRequestData):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "LUNO___SPOT")

    def _get_tick(
        self,
        symbol: str,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        path = "GET /ticker"
        return self._request_prepare(
            path,
            params={"pair": symbol},
            extra_data=extra_data,
            request_type="get_tick",
            symbol=symbol,
        )

    @staticmethod
    def _get_tick_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        return [input_data], True

    def get_tick(self, symbol: str, extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_tick(self, symbol: str, extra_data: Any = None, **kwargs: Any) -> None:
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_depth(
        self,
        symbol: str,
        count: int = 20,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        path = "/orderbook"
        return self._request_prepare(
            path,
            params={"pair": symbol},
            extra_data=extra_data,
            request_type="get_depth",
            symbol=symbol,
        )

    @staticmethod
    def _get_depth_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        return [input_data], True

    def get_depth(self, symbol: str, count: int = 20, extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_depth(
        self,
        symbol: str,
        count: int = 20,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> None:
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_kline(
        self,
        symbol: str,
        period: str,
        count: int = 20,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        path = "/candles"
        since = int((time.time() - 86400) * 1000)
        duration = self._exchange_data.get_period(period)
        return self._request_prepare(
            path,
            params={"pair": symbol, "since": since, "duration": duration},
            extra_data=extra_data,
            request_type="get_kline",
            symbol=symbol,
        )

    @staticmethod
    def _get_kline_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        klines = input_data.get("candles", []) if isinstance(input_data, dict) else []
        return [klines], True

    def get_kline(
        self,
        symbol: str,
        period: str,
        count: int = 20,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_kline(
        self,
        symbol: str,
        period: str,
        count: int = 20,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_exchange_info(
        self,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        path = "/markets"
        return self._request_prepare(
            path,
            params={},
            extra_data=extra_data,
            request_type="get_exchange_info",
            symbol="",
        )

    @staticmethod
    def _get_exchange_info_normalize_function(
        input_data: Any,
        extra_data: Any,
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        markets = input_data.get("markets", []) if isinstance(input_data, dict) else []
        return [markets], True

    def get_exchange_info(self, extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_balance(
        self,
        symbol: str | None = None,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        path = "/balance"
        return self._request_prepare(
            path,
            params={},
            extra_data=extra_data,
            request_type="get_balance",
            symbol=symbol or "",
        )

    @staticmethod
    def _get_balance_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        return [input_data], True

    def get_balance(self, symbol: str | None = None, extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_balance(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_account(
        self,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        path = "/balance"
        return self._request_prepare(
            path,
            params={},
            extra_data=extra_data,
            request_type="get_account",
            symbol="",
        )

    @staticmethod
    def _get_account_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        return [input_data], True

    def get_account(self, symbol: str = "ALL", extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_account(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _make_order(
        self,
        symbol: str,
        volume: float,
        price: float,
        order_type: str,
        offset: str = "open",
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, str], Any]:
        path = "POST /postorder"
        side = "BID" if "buy" in order_type.lower() else "ASK"
        params = {
            "pair": symbol,
            "type": side,
            "volume": str(volume),
            "price": str(price),
        }
        return self._request_prepare(
            path,
            params=params,
            extra_data=extra_data,
            request_type="make_order",
            symbol=symbol,
        )

    @staticmethod
    def _make_order_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        return [input_data], True

    def make_order(
        self,
        symbol: str,
        volume: float,
        price: float,
        order_type: str,
        offset: str = "open",
        post_only: bool = False,
        client_order_id: str | None = None,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._make_order(
            symbol,
            volume,
            price,
            order_type,
            offset,
            extra_data,
            **kwargs,
        )
        return self.request(path, params=params, extra_data=extra_data)

    def _cancel_order(
        self,
        symbol: str,
        order_id: str,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, str], Any]:
        path = "POST /stoporder"
        params = {"order_id": order_id}
        return self._request_prepare(
            path,
            params=params,
            extra_data=extra_data,
            request_type="cancel_order",
            symbol=symbol,
            order_id=order_id,
        )

    def cancel_order(
        self,
        symbol: str,
        order_id: str,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._cancel_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _request_prepare(
        self,
        path: str,
        params: dict | None = None,
        extra_data: Any = None,
        request_type: str = "",
        symbol: str = "",
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        from bt_api_base.functions.utils import update_extra_data

        extra_data = update_extra_data(
            extra_data,
            request_type=request_type,
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=getattr(self, f"_{request_type}_normalize_function"),
        )
        return path, params or {}, extra_data
