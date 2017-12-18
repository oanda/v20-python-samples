from datetime import datetime
import argparse
import common.args
import v20.transaction

def add_replace_order_id_argument(parser):
    """
    Add an argument to the parser for replacing an existing Order
    """
    parser.add_argument(
        "--replace-order-id", "-r",
        help=(
            "The ID of the Order to replace, only provided if the intent is to "
            "replace an existing pending Order. If prepended "
            "with an '@', this will be interpreted as a client Order ID"
        )
    )


class OrderArguments(object):
    """
    OrderArguments is a wrapper that manages adding command line parameters 
    used to configure Order creation
    """

    def __init__(self, parser):
        # Store the argument parser to add arguments to
        self.parser = parser

        # The parsed_args contains all of the parameters parsed for order
        # creation
        self.parsed_args = {}

        # The list of param_parsers are used to automatically interpret
        # order arguments that have been added
        self.param_parsers = []

        # The default formatter for arguments that are parsed as datetimes
        self.datetime_formatter = lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%S.000000000Z")


    def set_datetime_formatter(self, datetime_formatter):
        """
        Provide an alternate implementation of a datetime formatter
        """
        self.datetime_formatter = datetime_formatter

    def parse_arguments(self, args):
        """
        Call each param parser with the parsed arguments to extract the value
        into the parsed_args
        """
        for parser in self.param_parsers:
            parser(args)


    def add_trade_id(self):
        self.parser.add_argument(
            "tradeid",
            help=(
                "The ID of the Trade to create an Order for. If prepended "
                "with an '@', this will be interpreted as a client Trade ID"
            )
        )

        self.param_parsers.append(
            lambda args: self.parse_trade_id(args)
        )


    def parse_trade_id(self, args):
        if args.tradeid is None:
            return

        if args.tradeid[0] == '@':
            self.parsed_args["clientTradeID"] = args.tradeid[1:]
        else:
            self.parsed_args["tradeID"] = args.tradeid


    def add_instrument(self):
        self.parser.add_argument(
            "instrument",
            type=common.args.instrument,
            help="The instrument to place the Order for"
        )

        self.param_parsers.append(
            lambda args: self.parse_instrument(args)
        )


    def parse_instrument(self, args):
        if args.instrument is None:
            return

        self.parsed_args["instrument"] = args.instrument


    def add_units(self):
        self.parser.add_argument(
            "units",
            help=(
                "The number of units for the Order. "
                "Negative values indicate sell, Positive values indicate buy"
            )
        )

        self.param_parsers.append(
            lambda args: self.parse_units(args)
        )


    def parse_units(self, args):
        if args.units is None:
            return

        self.parsed_args["units"] = args.units


    def add_price(self):
        self.parser.add_argument(
            "price",
            help="The price threshold for the Order"
        )

        self.param_parsers.append(
            lambda args: self.parse_price(args)
        )


    def parse_price(self, args):
        if args.price is None:
            return

        self.parsed_args["price"] = args.price


    def add_distance(self):
        self.parser.add_argument(
            "distance",
            help="The price distance for the Order"
        )

        self.param_parsers.append(
            lambda args: self.parse_distance(args)
        )


    def parse_distance(self, args):
        if args.distance is None:
            return

        self.parsed_args["distance"] = args.distance


    def add_time_in_force(self, choices=["FOK", "IOC", "GTC", "GFD", "GTD"]):
        self.parser.add_argument(
            "--time-in-force", "--tif",
            choices=choices,
            help="The time-in-force to use for the Order"
        )

        if "GTD" in choices:
            self.parser.add_argument(
                "--gtd-time",
                type=common.args.date_time(),
                help=(
                    "The date to use when the time-in-force is GTD. "
                    "Format is 'YYYY-MM-DD HH:MM:SS"
                )
            )

        self.param_parsers.append(
            lambda args: self.parse_time_in_force(args)
        )


    def parse_time_in_force(self, args):
        if args.time_in_force is None:
            return

        self.parsed_args["timeInForce"] = args.time_in_force

        if args.time_in_force != "GTD":
            return

        if args.gtd_time is None:
            self.parser.error(
                "must set --gtd-time \"YYYY-MM-DD HH:MM:SS\" when "
                "--time-in-force=GTD"
            )
            return
            
        self.parsed_args["gtdTime"] = self.datetime_formatter(args.gtd_time)
        

    def add_price_bound(self):
        self.parser.add_argument(
            "--price-bound", "-b",
            help="The worst price bound allowed for the Order"
        )

        self.param_parsers.append(
            lambda args: self.parse_price_bound(args)
        )
        

    def parse_price_bound(self, args):
        if args.price_bound is None:
            return

        self.parsed_args["priceBound"] = args.price_bound


    def add_position_fill(self):
        self.parser.add_argument(
            "--position-fill",
            choices=["DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"],
            required=False,
            help="Specification of how the Order may affect open positions."
        )

        self.param_parsers.append(
            lambda args: self.parse_position_fill(args)
        )


    def parse_position_fill(self, args):
        if args.position_fill is None:
            return

        self.parsed_args["positionFill"] = args.position_fill


    def add_client_order_extensions(self):
        self.parser.add_argument(
            "--client-order-id", "--coi",
            help="The client-provided ID to assign to the Order"
        )

        self.parser.add_argument(
            "--client-order-tag", "--cot",
            help="The client-provided tag to assign to the Order"
        )

        self.parser.add_argument(
            "--client-order-comment", "--coc",
            help="The client-provided comment to assign to the Order"
        )

        self.param_parsers.append(
            lambda args: self.parse_client_order_extensions(args)
        )


    def parse_client_order_extensions(self, args):
        if (args.client_order_id is None and
            args.client_order_tag is None and
            args.client_order_comment is None):
            return
        
        kwargs = {}

        if args.client_order_id is not None:
            kwargs["id"] = args.client_order_id

        if args.client_order_tag is not None:
            kwargs["tag"] = args.client_order_tag

        if args.client_order_comment is not None:
            kwargs["comment"] = args.client_order_comment

        self.parsed_args["clientExtensions"] = \
            v20.transaction.ClientExtensions(
                **kwargs
            )


    def add_client_trade_extensions(self):
        self.parser.add_argument(
            "--client-trade-id", "--cti",
            help="The client-provided ID to assign a Trade opened by the Order"
        )

        self.parser.add_argument(
            "--client-trade-tag", "--ctt",
            help=(
                "The client-provided tag to assign to a Trade opened by the "
                "Order"
            )
        )

        self.parser.add_argument(
            "--client-trade-comment", "--ctc",
            help=(
                "The client-provided comment to assign to a Trade opened by "
                "the Order"
            )
        )

        self.param_parsers.append(
            lambda args: self.parse_client_trade_extensions(args)
        )


    def parse_client_trade_extensions(self, args):
        if (args.client_trade_id is None and
            args.client_trade_tag is None and
            args.client_trade_comment is None):
            return None
        
        kwargs = {}

        if args.client_trade_id is not None:
            kwargs["id"] = args.client_trade_id

        if args.client_trade_tag is not None:
            kwargs["tag"] = args.client_trade_tag

        if args.client_trade_comment is not None:
            kwargs["comment"] = args.client_trade_comment

        self.parsed_args["tradeClientExtensions"] = \
            v20.transaction.ClientExtensions(
                **kwargs
            )


    def add_take_profit_on_fill(self):
        self.parser.add_argument(
            "--take-profit-price", "--tp",
            help=(
                "The price of the Take Profit to add to a Trade opened by this "
                "Order"
            )
        )

        self.param_parsers.append(
            lambda args: self.parse_take_profit_on_fill(args)
        )


    def parse_take_profit_on_fill(self, args):
        if args.take_profit_price is None:
            return
        
        kwargs = {}

        kwargs["price"] = args.take_profit_price

        self.parsed_args["takeProfitOnFill"] = \
            v20.transaction.TakeProfitDetails(**kwargs)


    def add_stop_loss_on_fill(self):
        self.parser.add_argument(
            "--stop-loss-price", "--sl",
            help=(
                "The price of the Stop Loss to add to a Trade opened by this "
                "Order"
            )
        )

        self.param_parsers.append(
            lambda args: self.parse_stop_loss_on_fill(args)
        )


    def parse_stop_loss_on_fill(self, args):
        if args.stop_loss_price is None:
            return
        
        kwargs = {}

        kwargs["price"] = args.stop_loss_price

        self.parsed_args["stopLossOnFill"] = \
            v20.transaction.StopLossDetails(**kwargs)


    def add_trailing_stop_loss_on_fill(self):
        self.parser.add_argument(
            "--trailing-stop-loss-distance", "--tsl",
            help=(
                "The price distance for the Trailing Stop Loss to add to a "
                "Trade opened by this Order"
            )
        )

        self.param_parsers.append(
            lambda args: self.parse_trailing_stop_loss_on_fill(args)
        )


    def parse_trailing_stop_loss_on_fill(self, args):
        if args.trailing_stop_loss_distance is None:
            return
        
        kwargs = {}

        kwargs["distance"] = args.stop_loss_distance

        self.parsed_args["trailingStopLossOnFill"] = \
            v20.transaction.TrailingStopLossDetails(
                **kwargs
            )
