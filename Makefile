# Makefile with single task for running the defined tests
#
test:
	python tests/test_hypercat.py

build_dist:
	python setup.py sdist bdist_wheel

clean:
	python setup.py clean

default: test

.PHONY: test build_dist
