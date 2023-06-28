.PHONY: test
test:
	pytest ./tests

package:
	python setup.py sdist bdist_wheel --plat-name=$(OS)

publish: package
	twine upload