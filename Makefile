UV = uv

PROJECT = src

install:
	...


run:
	$(UV) run python -m $(PROJECT)


clean:
	find . -type d -name __pycache__ -exec rm -r {} +


run_test:
	$(UV) run python -m test_project