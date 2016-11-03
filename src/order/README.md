# Order Scripts

## Get Order

The script to get the details of a single Order is implemented in `get.py`. It
may be used to fetch an Order in any state (pending, cancelled, filled). It can
be executed directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/get.py
(env)user@host: ~/v20-python-samples$ v20-order-get
```
## Get Pending Orders

The script to get the details of all currently pending Order in the active
Account is implemented in `list_pending.py`.  It can be executed directly or
with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/list_pending.py
(env)user@host: ~/v20-python-samples$ v20-order-list-pending
```

## Cancel Order(s)

The script to cancel a pending Order in the active Account is implemented in
`cancel.py`. It can be used to cancel a single Order or all currently pending
Orders. It can be executed directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/cancel.py
(env)user@host: ~/v20-python-samples$ v20-order-cancel
```

## Set Order Client Extensions

The script to set the client extensions for a pending Order in the active
Account is implemented in `set_client_extensions.py`. It can be executed
directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/set_client_extensions.py
(env)user@host: ~/v20-python-samples$ v20-order-set-client-extensions
```

## Create Market Order

The script to create a Market Order in the active Account is implemented in
`market.py`. It can be executed directly or with the provided entry point
alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/market.py
(env)user@host: ~/v20-python-samples$ v20-order-market
```

## Create/Replace Entry Order

The script to create or replace an Entry Order in the active Account is
implemented in `entry.py`. It can be executed directly or with the provided
entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/entry.py
(env)user@host: ~/v20-python-samples$ v20-order-entry
```

## Create/Replace Limit Order

The script to create or replace a Limit Order in the active Account is
implemented in `limit.py`. It can be executed directly or with the provided
entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/limit.py
(env)user@host: ~/v20-python-samples$ v20-order-limit
```

## Create/Replace Stop Order

The script to create or replace a Stop Order in the active Account is
implemented in `stop.py`. It can be executed directly or with the provided
entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/stop.py
(env)user@host: ~/v20-python-samples$ v20-order-stop
```

## Create/Replace Take Profit Order

The script to create or replace a Take Profit Order in the active Account is
implemented in `take_profit.py`. It can be executed directly or with the
provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/take_profit.py
(env)user@host: ~/v20-python-samples$ v20-order-take-profit
```

## Create/Replace Stop Loss Order

The script to create or replace a Stop Loss Order in the active Account is
implemented in `stop_loss.py`. It can be executed directly or with the provided
entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/stop_loss.py
(env)user@host: ~/v20-python-samples$ v20-order-stop-loss
```

## Create/Replace Trailing Stop Loss Order

The script to create or replace a Trailing Stop Loss Order in the active
Account is implemented in `trailing_stop_loss.py`. It can be executed directly
or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/order/trailing_stop_loss.py
(env)user@host: ~/v20-python-samples$ v20-order-trailing-stop-loss
```
