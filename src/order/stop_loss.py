#!/usr/bin/env python

import argparse
import common.config
from .args import OrderArguments, add_replace_order_id_argument
from .view import print_order_create_response_transactions


def main():
    """
    Create or replace an OANDA Stop Loss Order in an Account based on the
    provided command-line arguments.
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    #
    # Add the argument to support replacing an existing argument
    #
    add_replace_order_id_argument(parser)

    #
    # Add the command line arguments required for a Limit Order
    #
    orderArgs = OrderArguments(parser)
    orderArgs.add_trade_id()
    orderArgs.add_price()
    orderArgs.add_time_in_force(["GTD", "GFD", "GTC"])
    orderArgs.add_client_order_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Extract the Limit Order parameters from the parsed arguments
    #
    orderArgs.parse_arguments(args)

    if args.replace_order_id is not None:
        #
        # Submit the request to cancel and replace a Stop Loss Order
        #
        response = api.order.stop_loss_replace(
            args.config.active_account,
            args.replace_order_id,
            **orderArgs.parsed_args
        )
    else:
        #
        # Submit the request to create a Stop Loss Order
        #
        response = api.order.stop_loss(
            args.config.active_account,
            **orderArgs.parsed_args
        )

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
