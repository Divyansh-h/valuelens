.PHONY: help install test run-pipeline dashboard clean

# Default target
help:
	@echo "ValueLens Makefile"
	@echo "------------------"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install       Install all dependencies from requirements.txt"
	@echo "  test          Run the automated pytest End-to-End test suite"
	@echo "  run-pipeline  Execute the full analytical pipeline from end to end"
	@echo "  dashboard     Launch the interactive Streamlit dashboard"
	@echo "  clean         Remove cached files and python bytecode"

install:
	pip install --upgrade pip
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

test:
	pytest tests/

run-pipeline:
	python run_pipeline.py

dashboard:
	streamlit run app.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
