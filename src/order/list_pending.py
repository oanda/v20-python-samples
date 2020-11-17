#!/usr/bin/env python

import argparse
import common.config


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
        "--verbose", "-v",
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

    if not args.summary:
        print("-" * 80)

    for order in orders:
        if args.summary:
            print(order.title())
        else:
            print(order.yaml(True))
            print("-" * 80)


if __name__ == "__main__":
    main()
