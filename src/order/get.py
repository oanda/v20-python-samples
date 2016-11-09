#!/usr/bin/env python

import argparse
import common.config
import common.view


def main():
    """
    Get the details of an Order in an Account
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    parser.add_argument(
        "orderid",
        help=(
            "The ID of the Order to get. If prepended "
            "with an '@', this will be interpreted as a client Order ID"
        )
    )

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Submit the request to create the Market Order
    #
    response = api.order.get(
        args.config.active_account,
        args.orderid
    )

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    order = response.get("order", 200)

    print(order)


if __name__ == "__main__":
    main()
