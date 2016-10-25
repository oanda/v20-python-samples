#!/usr/bin/env python

import argparse
import common.config
from args import OrderArguments
from v20.order import StopOrderRequest
from view import print_order_create_response_transactions


def main():
    """
    Create an OANDA Stop Order in an Account based on the provided
    command-line arguments.
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    #
    # Add the command line arguments required for a Stop Order
    #
    stopOrderArgs = OrderArguments(parser)
    stopOrderArgs.add_instrument()
    stopOrderArgs.add_units()
    stopOrderArgs.add_price()
    stopOrderArgs.add_price_bound()
    stopOrderArgs.add_time_in_force()
    stopOrderArgs.add_position_fill()
    stopOrderArgs.add_take_profit_on_fill()
    stopOrderArgs.add_stop_loss_on_fill()
    stopOrderArgs.add_trailing_stop_loss_on_fill()
    stopOrderArgs.add_client_order_extensions()
    stopOrderArgs.add_client_trade_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Extract the Stop Order parameters from the parsed arguments
    #
    stopOrderArgs.parse_arguments(args)

    #
    # Submit the request to create the Stop Order
    #
    response = api.order.stop(
        args.config.active_account,
        **stopOrderArgs.order_request
    )

    print "Response: {} ({})".format(response.status, response.reason)
    print

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
