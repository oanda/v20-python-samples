# Account Samples 

The Account scripts are sample programs that interact with the v20 REST API
Account endpoints described at
http://developer.oanda.com/rest-live-v20/account-ep/. 

## Account Summary

The Account Summary script is implemented in `summary.py`, and is used
to fetch and display the summary of the `active_account` found in the v20
configuration file. It can be executed directly or with the provided entry
point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/summary.py
(env)user@host: ~/v20-python-samples$ v20-account-summary
```

## Account Details

The Account Details script is implemented in `details.py`, and is used to fetch
and display the full details (including open Trades, open Positions and pending
Orders) of the `active_account` found in the v20 configuration file. It can be
executed directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/details.py
(env)user@host: ~/v20-python-samples$ v20-account-details
```

## Account Instruments

The Account Instruments script is implemented in `instruments.py`, and is used
to fetch and display the list of tradeable instruments for the `active_account`
found in the v20 configuration file. It can be executed directly or with the
provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/instruments.py
(env)user@host: ~/v20-python-samples$ v20-account-instruments
```

## Polling for Account Changes

The Account Changes script is implemented in `changes.py`, and is used to fetch
and display the current Account state, and then poll repeatedly for changes to
it. This script provides a reference implementation for how OANDA recommends
that Account state be managed. It can be executed directly or with the provided
entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/changes.py
(env)user@host: ~/v20-python-samples$ v20-account-changes
```

## Account Configuration

The Account Configuration script is implemented in `configure.py`, and is used
to modify client Account configuration (alias or default margin rate).  It can
be executed directly or with the provided entry point alias:

```bash
(env)user@host: ~/v20-python-samples$ python src/account/configuration.py
(env)user@host: ~/v20-python-samples$ v20-account-configuration
```
