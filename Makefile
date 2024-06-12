init:
	pip install -r requirements.txt

test:
	py.test module_tests

.PHONY: init test