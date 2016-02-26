# Makefile with single task for running the defined tests
#
test:
	python tests/test_hypercat.py

default: test

.PHONY: test
