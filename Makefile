.PHONY: bootstrap
bootstrap: bootstrap-python3

bootstrap-python3:
	virtualenv -p python3 env
	env/bin/pip install -r requirements/base.txt

bootstrap-python2:
	virtualenv env-python2
	env-python2/bin/pip install -r requirements/base.txt

