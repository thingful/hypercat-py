# Makefile with single task for running the defined tests
#
test:
	python tests/test_hypercat.py

info:
	python setup.py egg_info

build_dist:
	python setup.py sdist bdist_wheel

clean:
	python setup.py clean
	rm -rf dist/*

publish: build_dist
	twine upload dist/*

default: test

.PHONY: test build_dist clean publish
