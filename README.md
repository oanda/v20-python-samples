# v20-python-samples

Sample python code that uses the v20 python library

Setup
=====

The setup procedure describes how to create a virtualenv appropriate for
running the v20 sample code.

```
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

Entering the v20 environment
============================

The v20-python-samples virtualenv must be activated to ensure that the current
enviroment is set up correctly to run the sample code. This is done using the
virualenv's activate script:

```
user@host: ~/v20-python-samples$ source env/bin/activate
(env)user@host: ~/v20-python-samples$
```

The "(env)" prefix found in the prompt indicates that we are using the
virtualenv "env".  To leave the virtualenv, run the deactivate function:

```
(env)user@host: ~/v20-python-samples$ deactivate
user@host: ~/v20-python-samples$ 
```


