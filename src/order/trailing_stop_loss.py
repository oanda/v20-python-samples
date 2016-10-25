#!/usr/bin/env python

import argparse
import common.config
from args import OrderArguments
from view import print_order_create_response_transactions
from v20.order import TrailingStopLossOrderRequest


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
    tslOrderArgs = OrderArguments(parser)
    tslOrderArgs.add_trade_id()
    tslOrderArgs.add_distance()
    tslOrderArgs.add_time_in_force(["GTD", "GFD", "GTC"])
    tslOrderArgs.add_client_order_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Extract the Limit Order parameters from the parsed arguments
    #
    tslOrderArgs.parse_arguments(args)

    #
    # Submit the request to create the Limit Order
    #
    response = api.order.create(
        args.config.active_account,
        order=TrailingStopLossOrderRequest(**tslOrderArgs.order_request)
    )

    print "Response: {} ({})".format(response.status, response.reason)
    print

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
