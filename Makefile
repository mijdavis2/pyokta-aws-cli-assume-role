clean:
	rm -rf build; rm -rf dist; rm -rf pyokta_aws_cli_assume_role.egg-info

build: clean
	python setup.py sdist bdist_wheel

