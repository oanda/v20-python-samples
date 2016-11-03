# Trade Scripts

## Get specific Trade or all open Trades

The script to get a specific Trade or all open Trades in an Account is
implemented in `get.py`. It can be executed directly or with the provided
entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/trade/get.py
(env)user@host: ~/v20-python-samples$ v20-trade-get
```

## Close an open Trade

The script to close (fully or paritally) an open Trade in an Account is
implemented in `close.py`. It can be executed directly or with the provided entry
point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/trade/close.py
(env)user@host: ~/v20-python-samples$ v20-trade-close
```

## Set Trade Client Extensions

The script to set the client extensions for an open Trade in the active Account
is implemented in `set_client_extensions.py`. It can be executed directly or
with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/trade/set_client_extensions.py
(env)user@host: ~/v20-python-samples$ v20-trade-set-client-extensions
```
