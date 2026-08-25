# Makefile for Resume ATS Score Checker
# Developed by Vikram TRIVIKRAM

.PHONY: help install run test lint clean docker-build docker-run

help:
	@echo "Resume ATS Score Checker - Makefile"
	@echo "Developed by Vikram TRIVIKRAM"
	@echo ""
	@echo "Available commands:"
	@echo "  make help         - Show this help message"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the Flask development server"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linting checks"
	@echo "  make clean        - Remove temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	python app.py

test:
	python -m pytest tests/ -v

lint:
	pip install flake8 pylint
	flake8 .
	pylint app.py

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .coverage htmlcov
	rm -rf *.pyc *.pyo *.pyd
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

docker-build:
	docker build -t resume-ats-checker .

docker-run:
	docker run -p 5000:5000 --env-file <(env | grep -E "ANTHROPIC_") resume-ats-checker

# Development shortcuts
dev: install run

# Production deployment helpers
build: docker-build
deploy: docker-build docker-run