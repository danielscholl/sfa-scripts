# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Run script: `uv run <script>.py`
- Run tests: `uv run pytest`
- Run specific test: `uv run pytest -xvs tests/test_<name>.py::test_<function>`
- Format code: `uv run black .`
- Check types: `uv run mypy .`

## Code Style Guidelines

- **Python**: Use Python 3.11+ syntax
- **Dependencies**: Specified in script headers with uv format (`# /// script dependencies = [...]`)
- **Formatting**: Follow Black code style (line length: 88 characters)
- **Imports**: Group imports as: standard library, third-party, local; alphabetically sorted within groups
- **Typing**: Use type hints for all function parameters and return values
- **Naming**: Use snake_case for variables/functions, PascalCase for classes
- **Error handling**: Use try/except blocks with specific exceptions; log errors appropriately
- **Documentation**: Use docstrings (Google style) for all functions and classes
- **Testing**: Write pytest tests for all functionality
- **Single file scripts**: Scripts should be runnable as standalone files using uv

## Context Priming 

```
READ README.md, then run git ls-files, and 'eza --git-ignore --tree' to understand the context of the project.
```