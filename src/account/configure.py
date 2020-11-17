#!/usr/bin/env python

import argparse
import common.config
from common.view import print_response_entity


def main():
    """
    Create an API context, and use it to fetch an Account state and then
    continually poll for changes to it.

    The configuration for the context and Account to fetch is parsed from the
    config file provided as an argument.
    """

    parser = argparse.ArgumentParser()

    #
    # The config object is initialized by the argument parser, and contains
    # the REST APID host, port, accountID, etc.
    #
    common.config.add_argument(parser)

    parser.add_argument(
        "--margin-rate",
        default=None,
        help="The new default margin rate for the Account"
    )

    parser.add_argument(
        "--alias",
        default=None,
        help="The new alias for the Account"
    )

    args = parser.parse_args()

    account_id = args.config.active_account

    #
    # The v20 config object creates the v20.Context for us based on the
    # contents of the config file.
    #
    api = args.config.create_context()

    kwargs = {}

    if args.alias is not None:
        kwargs["alias"] = args.alias

    if args.margin_rate is not None:
        kwargs["marginRate"] = args.margin_rate

    #
    # Fetch the details of the Account found in the config file
    #
    response = api.account.configure(account_id, **kwargs)

    if response.status == 200:
        print("Success")
        print("")

    print_response_entity(
        response,
        "200",
        "Configure Transaction",
        "configureTransaction"
    )


if __name__ == "__main__":
    main()
