#!/usr/bin/env python

from __future__ import print_function

import argparse
import common.config
from common.view import print_trades


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    args = parser.parse_args()

    account_id = args.config.active_account
    
    api = args.config.create_context()

    response = api.trade.list(account_id)

    trades = response.get("trades", 200)

    if len(trades) == 0:
        print("Account {} has no open Trades".format(account_id))
        return

    trades = sorted(trades, key=lambda t: int(t.id))

    print_trades(trades)

if __name__ == "__main__":
    main()
