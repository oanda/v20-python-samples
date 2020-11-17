#!/usr/bin/env python

import argparse
import common.config
import common.view


def main():
    """
    Create an API context, and use it to fetch and display the tradeable
    instruments for and Account.

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
    # Fetch the tradeable instruments for the Account found in the config file
    #
    response = api.account.instruments(account_id)

    #
    # Extract the list of Instruments from the response.
    #
    instruments = response.get("instruments", "200")

    instruments.sort(key=lambda i: i.name)

    def marginFmt(instrument):
        return "{:.0f}:1 ({})".format(
            1.0 / float(instrument.marginRate),
            instrument.marginRate
        )

    def pipFmt(instrument):
        location = float(10 ** instrument.pipLocation)
        return "{:.4f}".format(location)

    #
    # Print the details of the Account's tradeable instruments
    #
    common.view.print_collection(
        "{} Instruments".format(len(instruments)),
        instruments,
        [
            ("Name", lambda i: i.name),
            ("Type", lambda i: i.type),
            ("Pip", pipFmt),
            ("Margin Rate", marginFmt),
        ]
    )


if __name__ == "__main__":
    main()
