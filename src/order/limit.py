#!/usr/bin/env python

import argparse
import common.config
from args import OrderArguments
from view import print_order_create_response_transactions


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
    limitOrderArgs = OrderArguments(parser)
    limitOrderArgs.add_instrument()
    limitOrderArgs.add_units()
    limitOrderArgs.add_price()
    limitOrderArgs.add_time_in_force()
    limitOrderArgs.add_position_fill()
    limitOrderArgs.add_take_profit_on_fill()
    limitOrderArgs.add_stop_loss_on_fill()
    limitOrderArgs.add_trailing_stop_loss_on_fill()
    limitOrderArgs.add_client_order_extensions()
    limitOrderArgs.add_client_trade_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Extract the Limit Order parameters from the parsed arguments
    #
    limitOrderArgs.parse_arguments(args)

    #
    # Submit the request to create the Limit Order
    #
    response = api.order.limit(
        args.config.active_account,
        **limitOrderArgs.order_request
    )

    if response.status / 100 != 2:
        print "Error {}: {}".format (response.status, response.body)
        return
    
    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
