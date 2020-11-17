#!/usr/bin/env python

import argparse
import common.config
import common.view
from common.input import get_yn
from .view import print_orders


def main():
    """
    Cancel one or more Pending Orders in an Account
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    parser.add_argument(
        "--order-id", "-o",
        help=(
            "The ID of the Order to cancel. If prepended "
            "with an '@', this will be interpreted as a client Order ID"
        )
    )

    parser.add_argument(
        "--all", "-a",
        action="store_true",
        default=False,
        help="Flag to cancel all Orders in the Account"
    )

    args = parser.parse_args()

    account_id = args.config.active_account

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    if args.all:
        #
        # Get the list of all pending Orders
        #
        response = api.order.list_pending(account_id)

        orders = response.get("orders", 200)

        if len(orders) == 0:
            print("Account {} has no pending Orders to cancel".format(
                account_id
            ))
            return

        print_orders(orders)

        if not get_yn("Cancel all Orders?"):
            return

        #
        # Loop through the pending Orders and cancel each one
        #
        for order in orders:
            response = api.order.cancel(account_id, order.id)

            orderCancelTransaction = response.get(
                "orderCancelTransaction", 200
            )

            print(orderCancelTransaction.title())

    elif args.order_id is not None:

        #
        # Submit the request to create the Market Order
        #
        response = api.order.cancel(
            account_id,
            args.order_id
        )

        print("Response: {} ({})".format(response.status, response.reason))
        print("")

        common.view.print_response_entity(
            response, 200, "Order Cancel", "orderCancelTransaction"
        )

        common.view.print_response_entity(
            response, 404, "Order Cancel Reject",
            "orderCancelRejectTransaction"
        )
    else:
        parser.error("Must provide --order-id or --all")


if __name__ == "__main__":
    main()
