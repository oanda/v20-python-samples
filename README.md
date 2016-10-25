# v20-python-samples

This repo contains a suite of Python sample code that desmonstrates the use of
OANDA's v20 REST API along with OANDA's v20 bindings for Python.

## Setup

The following procedure describes how to create a virtualenv appropriate for
running the v20 sample code:

```bash
#
# Set up the virtualenv and install required packages
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


## Account Scripts

The Account scripts are sample programs that interact with the v20 REST API
Account endpoints described at
http://developer.oanda.com/rest-live-v20/account-ep/

### Account Summary

The Account Summary script is defined at `src/account/summary.py`, and is used
to fetch and display the summary of the `active_account` found in the v20
configuration file. It can be executed directly or with the provided entry
point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/summary.py
(env)user@host: ~/v20-python-samples$ v20-account-summary
```

### Account Details

The Account Details script is defined at `src/account/details.py`, and is used
to fetch and display the full details (including open Trades, open Positions
and pending Orders) of the `active_account` found in the v20 configuration
file. It can be executed directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/details.py
(env)user@host: ~/v20-python-samples$ v20-account-details
```

### Account Instruments

The Account Instruments script is defined at `src/account/instruments.py`, and
is used to fetch and display the list of tradeable instruments for the
`active_account` found in the v20 configuration file. It can be executed
directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/instruments.py
(env)user@host: ~/v20-python-samples$ v20-account-instruments
```


### Polling for Account Changes

The Account Changes script is defined at `src/account/changes.py`, and is used
to fetch and display the current Account state, and then poll repeatedly for
changes to it. This script provides a reference implementation for how OANDA
recommends that Account state be managed. It can be executed directly or with
the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/changes.py
(env)user@host: ~/v20-python-samples$ v20-account-changes
```


### Account Configuration

The Account Configuration script is defined at `src/account/configure.py`, and
is used to modify client Account configuration.  It can be executed directly or
with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/changes.py
(env)user@host: ~/v20-python-samples$ v20-account-changes
```


## Instrument Scripts

### Fetch Instrument Candlesticks

The script to fetch instrument candlesticks is defined at
`src/instrument/candles.py`.  It can be executed directly or with the provided
entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/instrument/candles.py
(env)user@host: ~/v20-python-samples$ v20-instrument-candles
```


### Poll Instrument Candlesticks

The script to poll instrument candlesticks is defined at
`src/instrument/candles_poll.py`. It uses curses to redraw the current candle
while it is being updated, and moves on to the next candle when the current
candle is completed. It can be executed directly or with the provided entry
point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/instrument/candles_poll.py
(env)user@host: ~/v20-python-samples$ v20-instrument-candles-poll
```


## Orders

### Create Market Order

### Create Market Order

