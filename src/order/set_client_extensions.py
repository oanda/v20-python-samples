#!/usr/bin/env python

import argparse
import common.config
import common.view
from .args import OrderArguments


def main():
    """
    Set the client extensions of an open Trade in an Account
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

    extnArgs = OrderArguments(parser)
    extnArgs.add_client_order_extensions()
    extnArgs.add_client_trade_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    extnArgs.parse_arguments(args)

    #
    # Submit the request to create the Market Order
    #
    response = api.order.set_client_extensions(
        args.config.active_account,
        args.orderid,
        **extnArgs.parsed_args
    )

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print(response.get(
        "orderClientExtensionsModifyTransaction", 200
    ))


if __name__ == "__main__":
    main()
