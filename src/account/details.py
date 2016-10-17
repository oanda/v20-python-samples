#!/usr/bin/env python

from __future__ import print_function

import argparse
import common.config
from common.view import print_entity, print_collection, print_trades
from common.view import print_positions, print_orders, print_trade_summaries


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    args = parser.parse_args()

    account_id = args.config.active_account
    
    api = args.config.create_context()

    response = api.account.get(account_id)

    account = response.get("account", "200")

    print_entity(
        account.title(),
        account
    )
    print()

    print_trade_summaries(account.trades)
    print()

    print_positions(account.positions)
    print()

    print_orders(account.orders)
    print()


if __name__ == "__main__":
    main()
