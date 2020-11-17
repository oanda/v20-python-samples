#!/usr/bin/env python

import argparse
import common.config
from .account import Account


def main():
    """
    Create an API context, and use it to fetch and display the state of an
    Account.

    The configuration for the context and Account to fetch is parsed from the
    config file provided as an argument.
    """

    parser = argparse.ArgumentParser()

    #
    # The config object is initialized by the argument parser, and contains
    # the REST APID host, port, accountID, etc.
    #
    common.config.add_argument(parser)

    args = parser.parse_args()

    account_id = args.config.active_account

    #
    # The v20 config object creates the v20.Context for us based on the
    # contents of the config file.
    #
    api = args.config.create_context()

    #
    # Fetch the details of the Account found in the config file
    #
    response = api.account.get(account_id)

    #
    # Extract the Account representation from the response.
    #
    account = Account(
        response.get("account", "200")
    )

    account.dump()


if __name__ == "__main__":
    main()
