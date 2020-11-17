#!/usr/bin/env python

import sys
import select
import argparse
import common.config
from .account import Account


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
        "--poll-interval",
        type=int,
        default=5,
        help="The number of seconds between polls for Account changes"
    )

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
    # Extract the Account representation from the response and use
    # it to create an Account wrapper
    #
    account = Account(
        response.get("account", "200")
    )

    def dump():
        account.dump()

        print("Press <ENTER> to see current state for Account {}".format(
            account.details.id
        ))

    dump()

    while True:
        i, _, _ = select.select([sys.stdin], [], [], args.poll_interval)

        if i:
            sys.stdin.readline()
            dump()

        #
        # Poll for all changes to the account since the last
        # Account Transaction ID that was seen
        #
        response = api.account.changes(
            account_id,
            sinceTransactionID=account.details.lastTransactionID
        )

        account.apply_changes(
            response.get(
                "changes",
                "200"
            )
        )

        account.apply_state(
            response.get(
                "state",
                "200"
            )
        )

        account.details.lastTransactionID = response.get(
            "lastTransactionID",
            "200"
        )


if __name__ == "__main__":
    main()
