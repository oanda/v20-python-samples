#!/usr/bin/env python

import argparse
import common.config
import common.view
import v20.transaction


def main():
    """
    Set the client extensions for an open Trade in an Account
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    parser.add_argument(
        "tradeid",
        help=(
            "The ID of the Trade to set the client extensions for. If "
            "prepended with an '@', this will be interpreted as a client "
            "Order ID"
        )
    )

    parser.add_argument(
        "--client-id",
        help="The client-provided ID to assign to the Trade"
    )

    parser.add_argument(
        "--tag",
        help="The client-provided tag to assign to the Trade"
    )

    parser.add_argument(
        "--comment",
        help="The client-provided comment to assign to the Trade"
    )

    args = parser.parse_args()

    if (args.client_id is None and
            args.tag is None and
            args.comment is None):
        parser.error("must provide at least one client extension to be set")

    clientExtensions = v20.transaction.ClientExtensions(
        id=args.client_id,
        comment=args.comment,
        tag=args.tag
    )

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    account_id = args.config.active_account

    #
    # Submit the request to create the Market Order
    #
    response = api.trade.set_client_extensions(
        account_id,
        args.tradeid,
        clientExtensions=clientExtensions
    )

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print(
        response.get(
            "tradeClientExtensionsModifyTransaction", 200
        )
    )


if __name__ == "__main__":
    main()
