.PHONY: test
test:
	pytest ./tests

# python setup.py sdist bdist_wheel --plat-name=$(OS) win_amd64 manylinux1_x86_64 macosx_10_9_x86_64
package:
	python setup.py bdist_wheel --plat-name $(OS)

publish: package
	twine upload dist/*.whl --verbose