# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Commands
- Setup: `poetry install --with dev`
- Run server: `poetry run python -m camera_collector.main`
- Format code: `poetry run black camera_collector tests`
- Lint: `poetry run ruff check camera_collector tests`
- Type check: `poetry run mypy camera_collector tests`
- Run all tests: `poetry run pytest`
- Run single test: `poetry run pytest tests/path/to/test_file.py::TestClass::test_function -v`
- Test with coverage: `poetry run pytest --cov=camera_collector --cov-report=term-missing`
- Pre-commit: `poetry run pre-commit run --all-files`

## Code Style Guidelines
- Use FastAPI and Pydantic for API and data validation
- Follow PEP 8 style guidelines, enforced by black and ruff
- Package structure follows standard Python package layout with src directory
- All functions must have type annotations
- Use async/await pattern consistently
- Document all functions with docstrings
- Exception handling via custom exception classes
- Prefer dependency injection
- Write tests using pytest with at least 80% coverage
- Imports organized in this order: stdlib, third-party, local
- Branch naming: feature/*, bugfix/*, release/*