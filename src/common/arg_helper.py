from datetime import datetime
import argparse
import v20.transaction

def instrument(i):
    return i.replace("/", "_")

def date_time(fmt="%Y-%m-%d %H:%M:%S"):
    def parse(s):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    return parse

def add_client_order_extensions(parser):
    parser.add_argument(
        "--client-order-id",
        help="The client-provided ID to assign to the Order"
    )

    parser.add_argument(
        "--client-order-tag",
        help="The client-provided tag to assign to the Order"
    )

    parser.add_argument(
        "--client-order-comment",
        help="The client-provided comment to assign to the Order"
    )

def parse_client_order_extensions(args):
    if (args.client_order_id is None and
        args.client_order_tag is None and
        args.client_order_comment is None):
        return None
    
    kwargs = {}

    if args.client_order_id is not None:
        kwargs["id"] = args.client_order_id

    if args.client_order_tag is not None:
        kwargs["tag"] = args.client_order_tag

    if args.client_order_comment is not None:
        kwargs["comment"] = args.client_order_comment

    return v20.transaction.ClientExtensions(**kwargs)
