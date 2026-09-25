UV = uv

PROJECT = src

install:
	unzip ./data/raw/vllm-0.10.1.zip


run:
	$(UV) run python -m $(PROJECT)


clean:
	rm -rf ./data/raw/vllm-0.10.1
	find . -type d -name __pycache__ -exec rm -r {} +


run_test:
	$(UV) run python -m test_project