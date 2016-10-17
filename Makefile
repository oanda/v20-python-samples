.PHONY: bootstrap
bootstrap:
	virtualenv env
	env/bin/pip install -r requirements.txt
