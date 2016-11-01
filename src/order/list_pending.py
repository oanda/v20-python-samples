#!/usr/bin/env python

import argparse
import common.config
from .view import print_orders


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    parser.add_argument(
        "--summary",
        dest="summary",
        action="store_true",
        help="Print a summary of the orders",
        default=True
    )

    parser.add_argument(
        "--details",
        dest="summary",
        help="Print details of the orders",
        action="store_false"
    )

    args = parser.parse_args()

    account_id = args.config.active_account
    
    api = args.config.create_context()

    response = api.order.list_pending(account_id)

    orders = response.get("orders", 200)

    if len(orders) == 0:
        print("Account {} has no pending Orders".format(account_id))
        return

    orders = sorted(orders, key=lambda o: int(o.id))

    if args.summary:
        print_orders(orders)
    else:
        for order in orders:
            print(order)

        

if __name__ == "__main__":
    main()
