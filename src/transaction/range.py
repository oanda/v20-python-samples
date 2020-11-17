#!/usr/bin/env python

import argparse
import common.config
import common.args


def main():
    """
    Poll Transactions for the active Account
    """

    parser = argparse.ArgumentParser()

    common.config.add_argument(parser)

    parser.add_argument(
        'fromid',
        help="The ID of the first Transaction to get"
    )

    parser.add_argument(
        'toid',
        help="The ID of the last Transaction to get"
    )

    parser.add_argument(
        '--type',
        action="append",
        help=(
            "Type filter for range request. This can be any Transaction type "
            "name or one of the groupings ORDER FUNDING ADMIN"
        )
    )

    args = parser.parse_args()

    api = args.config.create_context()

    filter = None

    if args.type is not None:
        filter = ",".join(args.type)

    account_id = args.config.active_account

    response = api.transaction.range(
        account_id,
        fromID=args.fromid,
        toID=args.toid,
        type=filter
    )

    for transaction in response.get("transactions", 200):
        print(transaction.title())


if __name__ == "__main__":
    main()
