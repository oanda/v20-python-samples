# Pricing Scripts

## Get/Poll Account Prices

The script to get current prices for the active Account implemented in
`get.py`.  It may be used to repeated poll for changes to the prices. It can be
executed directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/pricing/get.py
(env)user@host: ~/v20-python-samples$ v20-pricing-get
```
## Stream Account Prices

The script to stream Prices for the active Account is implemented in
`stream.py`.  It can be executed directly or with the provided entry point
alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/pricing/stream.py
(env)user@host: ~/v20-python-samples$ v20-pricing-stream
```

