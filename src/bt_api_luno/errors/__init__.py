from __future__ import annotations

from typing import Any

from bt_api_base.error import ErrorCategory, ErrorTranslator, UnifiedError, UnifiedErrorCode


class LunoErrorTranslator(ErrorTranslator):
    @classmethod
    def translate(cls, raw_error: dict[str, Any], venue: str) -> UnifiedError | None:
        message = str(raw_error.get("error") or raw_error.get("message") or "Unknown error")
        lower = message.lower()

        if "invalid" in lower and ("key" in lower or "api" in lower):
            code = UnifiedErrorCode.INVALID_API_KEY
            category = ErrorCategory.AUTH
        elif "signature" in lower or "auth" in lower:
            code = UnifiedErrorCode.INVALID_SIGNATURE
            category = ErrorCategory.AUTH
        elif "balance" in lower or "insufficient" in lower:
            code = UnifiedErrorCode.INSUFFICIENT_BALANCE
            category = ErrorCategory.BUSINESS
        elif "rate" in lower or "limit" in lower:
            code = UnifiedErrorCode.RATE_LIMIT_EXCEEDED
            category = ErrorCategory.RATE_LIMIT
        elif "order" in lower and "not found" in lower:
            code = UnifiedErrorCode.ORDER_NOT_FOUND
            category = ErrorCategory.BUSINESS
        elif "market" in lower and "closed" in lower:
            code = UnifiedErrorCode.EXCHANGE_MAINTENANCE
            category = ErrorCategory.SYSTEM
        else:
            code = UnifiedErrorCode.INTERNAL_ERROR
            category = ErrorCategory.SYSTEM

        return UnifiedError(
            code=code,
            category=category,
            venue=venue,
            message=message,
            original_error=str(raw_error),
            context={"raw_response": raw_error},
        )

    @staticmethod
    def is_error(response: dict[str, Any]) -> bool:
        if not isinstance(response, dict):
            return False
        return bool(response.get("error") or response.get("message"))


__all__ = ["LunoErrorTranslator"]
