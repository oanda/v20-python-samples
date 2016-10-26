#!/usr/bin/env python

from __future__ import print_function

import argparse
import common.config
from common.input import get_yn
from view import print_orders


def main():
    """
    Cancel all Orders pending within an Account.
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    args = parser.parse_args()

    api = args.config.create_context()

    account_id = args.config.active_account

    #
    # Get the list of all pending Orders
    #
    response = api.order.list_pending(account_id)

    orders = response.get("orders", 200)

    if len(orders) == 0:
        print("Account {} has no pending Orders to cancel".format(account_id))
        return

    print_orders(orders)

    if not get_yn("Cancel all Orders?"):
        return

    #
    # Loop through the pending Orders and cancel each one
    #
    for order in orders:
        response = api.order.cancel(account_id, order.id)

        orderCancelTransaction = response.get("orderCancelTransaction", 200)

        print(orderCancelTransaction.title())

if __name__ == "__main__":
    main()
