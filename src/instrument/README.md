# Instrument Scripts

## Fetch Instrument Candlesticks

The script to fetch instrument candlesticks is implemented in `candles.py`.  It
can be executed directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/instrument/candles.py
(env)user@host: ~/v20-python-samples$ v20-instrument-candles
```

## Poll Instrument Candlesticks

The script to poll instrument candlesticks is implemented in `candles_poll.py`.
It uses curses to redraw the current candle while it is being updated, and
moves on to the next candle when the current candle is completed. It can be
executed directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/instrument/candles_poll.py
(env)user@host: ~/v20-python-samples$ v20-instrument-candles-poll
```
