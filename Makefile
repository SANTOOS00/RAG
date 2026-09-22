UV = uv

PROJECT = src

install:
	...


run:
	$(UV) run python -m $(PROJECT)


clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -r {} +
	