#!/usr/bin/env python

import argparse
import common.config
from args import OrderArguments
from view import print_order_create_response_transactions
from v20.order import StopLossOrderRequest


def main():
    """
    Create an OANDA Limit Order in an Account based on the provided
    command-line arguments.
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    #
    # Add the command line arguments required for a Limit Order
    #
    slOrderArgs = OrderArguments(parser)
    slOrderArgs.add_trade_id()
    slOrderArgs.add_price()
    slOrderArgs.add_time_in_force(["GTD", "GFD", "GTC"])
    slOrderArgs.add_client_order_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Extract the Limit Order parameters from the parsed arguments
    #
    slOrderArgs.parse_arguments(args)

    #
    # Submit the request to create the Limit Order
    #
    response = api.order.create(
        args.config.active_account,
        order=StopLossOrderRequest(**slOrderArgs.order_request)
    )

    print "Response: {} ({})".format(response.status, response.reason)
    print

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
