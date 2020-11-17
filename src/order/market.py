#!/usr/bin/env python

import argparse
import common.config
from .args import OrderArguments
from .view import print_order_create_response_transactions


def main():
    """
    Create a Market Order in an Account based on the provided command-line
    arguments.
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    #
    # Add the command line arguments required for a Market Order
    #
    marketOrderArgs = OrderArguments(parser)
    marketOrderArgs.add_instrument()
    marketOrderArgs.add_units()
    marketOrderArgs.add_time_in_force(["FOK", "IOC"])
    marketOrderArgs.add_price_bound()
    marketOrderArgs.add_position_fill()
    marketOrderArgs.add_take_profit_on_fill()
    marketOrderArgs.add_stop_loss_on_fill()
    marketOrderArgs.add_trailing_stop_loss_on_fill()
    marketOrderArgs.add_client_order_extensions()
    marketOrderArgs.add_client_trade_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Extract the Market order parameters from the parsed arguments
    #
    marketOrderArgs.parse_arguments(args)

    #
    # Submit the request to create the Market Order
    #
    response = api.order.market(
        args.config.active_account,
        **marketOrderArgs.parsed_args
    )

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
