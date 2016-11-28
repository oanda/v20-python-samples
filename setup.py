from setuptools import setup, find_packages

setup(
    name='v20-python-samples',
    version='0.1.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'v20-configure = configure:main',
            'v20-market-order-full-example = market_order_full_example:main',
            'v20-account-details = account.details:main',
            'v20-account-summary = account.summary:main',
            'v20-account-instruments = account.instruments:main',
            'v20-account-changes = account.changes:main',
            'v20-account-configure = account.configure:main',
            'v20-instrument-candles = instrument.candles:main',
            'v20-instrument-candles-poll = instrument.candles_poll:main',
            'v20-order-get = order.get:main',
            'v20-order-list-pending = order.list_pending:main',
            'v20-order-cancel = order.cancel:main',
            'v20-order-set-client-extensions = order.set_client_extensions:main',
            'v20-order-market = order.market:main',
            'v20-order-entry = order.entry:main',
            'v20-order-limit = order.limit:main',
            'v20-order-stop = order.stop:main',
            'v20-order-take-profit = order.take_profit:main',
            'v20-order-stop-loss = order.stop_loss:main',
            'v20-order-trailing-stop-loss = order.trailing_stop_loss:main',
            'v20-pricing-get = pricing.get:main',
            'v20-pricing-stream = pricing.stream:main',
            'v20-transaction-stream = transaction.stream:main',
            'v20-transaction-poll = transaction.poll:main',
            'v20-transaction-get = transaction.get:main',
            'v20-transaction-range = transaction.range:main',
            'v20-trade-get = trade.get:main',
            'v20-trade-close = trade.close:main',
            'v20-trade-set-client-extensions = trade.set_client_extensions:main',
            'v20-position-close = position.close:main',
        ]
    }
)

