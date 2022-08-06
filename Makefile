.PHONY: bootstrap
bootstrap: bootstrap-python3

bootstrap-python3:
	virtualenv -p python3 env
	env/bin/pip install -r requirements/base.txt
	echo "python version on ubuntu 22 will be 3.10. We need to upgrade something..."
	sed -i 's/if\ python_version_tuple/if True or python_version_tuple/g' env/lib/python3.10/site-packages/tabulate.py

bootstrap-python2:
	virtualenv env-python2
	echo "we don't do that here"
	exit 1
	env-python2/bin/pip install -r requirements/base.txt

