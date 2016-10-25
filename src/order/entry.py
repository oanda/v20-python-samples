#!/usr/bin/env python

import argparse
import common.config
from args import OrderArguments
from view import print_order_create_response_transactions


def main():
    """
    Create an OANDA Entry Order in an Account based on the provided
    command-line arguments.
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    #
    # Add the command line arguments required for an Entry Order
    #
    entryOrderArgs = OrderArguments(parser)
    entryOrderArgs.add_instrument()
    entryOrderArgs.add_units()
    entryOrderArgs.add_price()
    entryOrderArgs.add_price_bound()
    entryOrderArgs.add_time_in_force()
    entryOrderArgs.add_position_fill()
    entryOrderArgs.add_take_profit_on_fill()
    entryOrderArgs.add_stop_loss_on_fill()
    entryOrderArgs.add_trailing_stop_loss_on_fill()
    entryOrderArgs.add_client_order_extensions()
    entryOrderArgs.add_client_trade_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Extract the Entry Order parameters from the parsed arguments
    #
    entryOrderArgs.parse_arguments(args)

    #
    # Submit the request to create the Entry Order
    #
    response = api.order.market_if_touched(
        args.config.active_account,
        **entryOrderArgs.order_request
    )

    if response.status / 100 != 2:
        print "Error {}: {}".format (response.status, response.body)
        return
    
    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
