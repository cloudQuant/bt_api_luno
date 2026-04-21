from __future__ import annotations

import base64
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.feed import Feed

from ...exchange_data import LunoExchangeDataSpot


class LunoRequestData(Feed):
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "LUNO___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._exchange_data = LunoExchangeDataSpot()
        self._params = self._exchange_data
        self._params.rest_url = self._exchange_data.get_rest_url()
        self._params.rest_exchange_url = self._exchange_data.get_rest_url()
        self.api_key = kwargs.get("public_key") or kwargs.get("api_key") or ""
        self.secret = (
            kwargs.get("private_key") or kwargs.get("api_secret") or kwargs.get("secret_key") or ""
        )
        self._params.api_key = self.api_key
        self._params.api_secret = self.secret

    def _resolve_url(self, path: str) -> str:
        if path in ("/markets", "/candles"):
            return self._params.rest_exchange_url
        return self._params.rest_url

    def _resolve_method_and_path(self, path: str) -> tuple[str, str]:
        if " " in path:
            method, endpoint = path.split(" ", 1)
            return method.upper(), endpoint
        return "GET", path

    def _get_auth_headers(self) -> dict[str, str]:
        credentials = (
            f"{getattr(self._params, 'api_key', self.api_key)}:"
            f"{getattr(self._params, 'api_secret', self.secret)}"
        )
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {encoded}"}

    def request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        extra_data: dict[str, Any] | None = None,
        is_private: bool = False,
    ) -> RequestData:
        method, endpoint = self._resolve_method_and_path(path)
        response = self._http_client.request(
            method=method,
            url=f"{self._resolve_url(endpoint)}{endpoint}",
            headers=self._get_auth_headers() if is_private else None,
            params=params,
            json_data=params if method in {"POST", "PUT", "PATCH", "DELETE"} else None,
        )
        return RequestData(response, extra_data or {})

    async def async_request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        extra_data: dict[str, Any] | None = None,
        is_private: bool = False,
    ) -> RequestData:
        method, endpoint = self._resolve_method_and_path(path)
        response = await self._http_client.async_request(
            method=method,
            url=f"{self._resolve_url(endpoint)}{endpoint}",
            headers=self._get_auth_headers() if is_private else None,
            params=params,
            json_data=params if method in {"POST", "PUT", "PATCH", "DELETE"} else None,
        )
        return RequestData(response, extra_data or {})

    def _request_prepare(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        extra_data: dict[str, Any] | None = None,
        request_type: str = "",
        symbol: str = "",
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        payload = dict(extra_data or {})
        payload.update(
            {
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
            }
        )
        return path, params or {}, payload

    def push_data_to_queue(self, data: Any) -> None:
        if self.data_queue is not None:
            self.data_queue.put(data)

    def async_callback(self, future: Any) -> None:
        result = future.result()
        if result is not None:
            self.push_data_to_queue(result)

    def disconnect(self) -> None:
        self._http_client.close()


__all__ = ["LunoRequestData"]
