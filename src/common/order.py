import argparse
import arg_helper
import config

def add_order_request_args(OrderRequestType, parser):
    for property in OrderRequestType._properties:
        if property.required:
            options = {
                "help": property.description
            }

            if property.typeName == "primitives.InstrumentName":
                options["type"] = arg_helper.parse_instrument

            if property.default:
                options["default"] = property.default
            else:
                options["default"] = argparse.SUPPRESS
                options["required"] = True

            parser.add_argument(
                "--{}".format(property.name),
                **options
            )

        elif property.typeClass == "primitive":

            options = {
                "help": property.description
            }

            if property.typeName == "primitives.InstrumentName":
                options["type"] = arg_helper.parse_instrument

            if property.default:
                options["default"] = property.default
            else:
                options["default"] = argparse.SUPPRESS

            parser.add_argument(
                "--{}".format(property.name),
                **options
            )

def create_order(OrderRequestType):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    config.add_argument(parser)

    add_order_request_args(OrderRequestType, parser)

    args = parser.parse_args()

    args_dict = vars(args)

    order_request = OrderRequestType(**args_dict)

    account_id = args.config.active_account

    api = args.config.create_context()

    response = api.order.create(account_id, order=order_request)

    print response
    try:
        orderCreateTransaction = response.get("orderCreateTransaction", 201)
        print_entity(orderCreateTransaction, title="Order Create")
    except:
        pass
         
    try:
        orderFillTransaction = response.get("orderFillTransaction", 201)
        print_entity(orderFillTransaction, title="Order Fill")
    except:
        pass
