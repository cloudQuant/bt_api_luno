"""Module-level docstring."""
from __future__ import annotations

from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry

from .registry_registration import register_luno as _register_luno

__version__ = "0.1.0"


def register_plugin(
    registry: type[ExchangeRegistry],
    runtime_factory: type[GatewayRuntimeRegistrar],
) -> PluginInfo:
    """register_plugin function"""
    _register_luno(registry)
    return plugin_info()


def register_luno(
    registry: type[ExchangeRegistry] = ExchangeRegistry,
    runtime_factory: type[GatewayRuntimeRegistrar] = GatewayRuntimeRegistrar,
) -> PluginInfo:
    """register_luno function"""
    return register_plugin(registry, runtime_factory)


def plugin_info() -> PluginInfo:
    """plugin_info function"""
    return PluginInfo(
        name="bt_api_luno",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("LUNO___SPOT",),
        supported_asset_types=("SPOT",),
    )


__all__ = ["plugin_info", "register_luno", "register_plugin"]
