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
        'id',
        help="The ID of the Transaction to get"
    )

    args = parser.parse_args()

    api = args.config.create_context()

    account_id = args.config.active_account

    response = api.transaction.get(account_id, args.id)

    print(response.get("transaction", 200))


if __name__ == "__main__":
    main()
