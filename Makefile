clean:
	pip uninstall -y pyokta-aws-cli-assume-role; \
	rm -rf pyokta_aws/__pycache__/; \
	rm -rf pyokta_aws/**/__pycache__/; \
	rm -rf pyokta_aws/**/*.pyc; \
	rm -rf tests/__pycache__/; \
	rm -rf tests/**/__pycache__/; \
	rm -rf tests/**/*.pyc; \
	rm -rf build; \
	rm -rf dist; \
	rm -rf pyokta_aws_cli_assume_role.egg-info

build: clean
	python setup.py sdist bdist_wheel

test: build
	tox

deploy: test
	git push origin master
	twine upload dist/*

install: build
	pip install -e ./
