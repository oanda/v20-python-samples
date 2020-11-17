def price_to_string(price):
    return "{} ({}) {}/{}".format(
        price.instrument,
        price.time,
        price.bids[0].price,
        price.asks[0].price
    )


def heartbeat_to_string(heartbeat):
    return "HEARTBEAT ({})".format(
        heartbeat.time
    )
