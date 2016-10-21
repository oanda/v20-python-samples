#!/usr/bin/env python

from __future__ import print_function

import argparse
import common.config
from common.view import print_orders


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    args = parser.parse_args()

    account_id = args.config.active_account
    
    api = args.config.create_context()

    response = api.order.list_pending(account_id)

    orders = response.get("orders", 200)

    if len(orders) == 0:
        print("Account {} has no pending Orders".format(account_id))
        return

    orders = sorted(orders, key=lambda o: int(o.id))

    print_orders(orders)

if __name__ == "__main__":
    main()
