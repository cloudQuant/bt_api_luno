# bt_api_luno

Luno exchange adapter for bt_api.

## Installation

```bash
pip install bt_api_luno
```

## Usage

```python
from bt_api_luno import register_luno
register_luno()

from bt_api_py import BtApi
api = BtApi(exchange_kwargs={"LUNO___SPOT": {"api_key": "...", "secret": "..."}})
ticker = api.get_tick("LUNO___SPOT", "XBTZAR")
```
