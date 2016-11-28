# v20-python-samples

This repo contains a suite of Python sample code that desmonstrates the use of
OANDA's v20 REST API along with OANDA's v20 bindings for Python.

## Setup

The following procedure describes how to create a virtualenv appropriate for
running the v20 sample code:

```bash
#
# Set up the virtualenv and install required packages. By default the
# virtualenv will be setup to use python3. If python2 is desired, use the make
# target "bootstrap-python2" and the virtualenv will be created under
# "env-python2"
#
user@host: ~/v20-python-samples$ make bootstrap

#
# Enter the virtualenv
#
user@host: ~/v20-python-samples$ source env/bin/activate

#
# Create the v20-* launch entry points in the virtualenv. These entry points
# are aliases for the scripts which use the v20 REST API to interact with an
# account (e.g. v20-market-order, v20-trades-list, etc.)
#
(env)user@host: ~/v20-python-samples$ python setup.py develop
```

## Entering the v20 environment

The v20-python-samples virtualenv must be activated to ensure that the current
enviroment is set up correctly to run the sample code. This is done using the
virualenv's activate script:

```bash
user@host: ~/v20-python-samples$ source env/bin/activate
(env)user@host: ~/v20-python-samples$
```

The "(env)" prefix found in the prompt indicates that we are using the
virtualenv "env".  To leave the virtualenv, run the deactivate function:

```bash
(env)user@host: ~/v20-python-samples$ deactivate
user@host: ~/v20-python-samples$ 
```


## Configuration-free Example

Most of the examples provided use a v20.conf discussed below. For a full
example of how to create and use a v20 API context without the configuration
wrapper, please examine `src/market_order_full_example.py`. This program
enables the creation of a limited Market Order solely based on command line
arguments.


## Configuration

Using OANDA's v20 REST API requires configuration to set up connections and 
interact with the endpoints. This configuration includes:

* API hostname
* API port
* API token
* username of client
* Account ID of account being manipulated

To simplify the management of this configuration, the v20 Python sample code
requires that a configuration file be created. All of the sample code loads
this configuration file prior to connecting to the v20 system.

### v20 Configuration File Format

The v20 configuration is stored in a YAML file that resembles the following:

```yaml
hostname: api-fxpractice.oanda.com
streaming_hostname: stream-fxpractice.oanda.com
port: 443
ssl: true
token: e6ab562b039325f12a026c6fdb7b71bb-b3d8721445817159410f01514acd19hbc
username: user
accounts:
- 101-001-100000-001
- 101-001-100000-002
active_account: 101-001-100000-001
```

### Generating v20 Configuration files

v20 configuration files may be generated manually, however a script is provided that
will generate one interactively located at `src/configure.py`.

To run it and generate a v20 configuration file, simply run:

```bash
(env)user@host: ~/v20-python-samples$ v20-configure
```

and follow the instructions.

### Using v20 Configuration files

There are several ways to load a v20 configuration file in each of v20 sample scripts:

#### 1. Run the script with the `--config` option 

The `--config` options allows you to specify the location of a valid v20 configuration file v20. Example: 

```bash
(env)user@host: ~/v20-python-samples$ v20-account-details --config /home/user/v20.conf
```

#### 2. Use the default v20 configuration file location

The default location for the v20 configuration file is `~/.v20.conf`. If a v20
configuration file exists in the default location, no `--config` option needs
to be used. Example:

```bash
# Looks for config file at ~/.v20.conf
(env)user@host: ~/v20-python-samples$ v20-account-details
```

#### 3. Set the location of the `V20_CONF` environment variable 

This `V20_CONF` environment variable changes what the default location of the
v20 configuration file is. If a configuration file exists in this location, no
`--config` option needs to be used. Example:

```bash
(env)user@host: ~/v20-python-samples$ export V20_CONF=/home/user/v20.conf
(env)user@host: ~/v20-python-samples$ v20-account-details
```


## Sample Code

Following is a listing of the sample code provided. More details can be found
in the READMEs provided in each src directory.

| Source File | Entry Point | Description |
| ----------- | ----------- | ----------- |
| `src/configure.py` | v20-configure | Create/update a v20.conf file |
| `src/market_order_full_example.py` | v20-market-order-full-example | Limited Market Order example that does not use the v20.conf file |
| `src/account/details.py` | v20-account-details | Get the details of the current active Account |
| `src/account/summary.py` | v20-account-summary | Get the summary of the current active Account |
| `src/account/instruments.py` | v20-account-instruments | Get the list of tradeable instruments for the current active Account |
| `src/account/changes.py` | v20-account-changes | Follow changes to the current active Account |
| `src/account/configure.py` | v20-account-configure | Set configuration in the current active Account |
| `src/instrument/candles.py` | v20-instrument-candles | Fetch candles for an instrument |
| `src/instrument/candles_poll.py` | v20-instrument-candles-poll | Fetch and poll for candle updates for an instrument |
| `src/order/get.py` | v20-order-get | Get the details of an order in the current active Account |
| `src/order/list_pending.py` | v20-order-list-pending | List all pending Orders for the current active Account |
| `src/order/cancel.py` | v20-order-cancel | Cancel a pending Order in the current active Account |
| `src/order/set_client_extensions.py` | v20-order-set-client-extensions | Set the client extensions for a pending Order in the current active Account |
| `src/order/market.py` | v20-order-market | Create a Market Order in the current active Account |
| `src/order/entry.py` | v20-order-entry | Create or replace an Entry Order in the current active Account |
| `src/order/limit.py` | v20-order-limit | Create or replace a Limit Order in the current active Account |
| `src/order/stop.py` | v20-order-stop | Create or replace a Stop Order in the current active Account |
| `src/order/take-profit.py` | v20-order-take-profit | Create or replace a Take Profit Order in the current active Account |
| `src/order/stop-loss.py` | v20-order-stop-loss | Create or replace a Stop Loss Order in the current active Account |
| `src/order/trailing-stop-loss.py` | v20-order-trailing-stop-loss | Create or replace a Trailing Stop Loss Order in the current active Account |
| `src/pricing/get.py` | v20-pricing-get | Fetch/poll the current Prices for a list of Instruments |
| `src/pricing/stream.py` | v20-pricing-stream | Stream Prices for a list of Instruments |
| `src/transaction/stream.py` | v20-transaction-stream | Stream Transactions for the current active Account |
| `src/transaction/poll.py` | v20-transaction-poll | Poll Transactions for the current active Account |
| `src/transaction/get.py` | v20-transaction-get | Get details for a Transaction in the current active Account |
| `src/transaction/range.py` | v20-transaction-range | Get a range of Transactions in the current active Account |
| `src/trade/get.py` | v20-trade-get | Get all open Trades or a specific Trade in the current active Account |
| `src/trade/close.py` | v20-trade-close | Close (partially or fully) a Trade in the current active Account |
| `src/trade/set_client_extensions.py` | v20-trade-set-client-extensions | Set the client extensions for an open Trade in the current active Account |
| `src/position/close.py` | v20-position-close | Close a position for an instrument in the current active Account |
