.PHONY: install test lint typecheck backtest research paper

install:
	uv sync --extra all

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src

backtest:
	uv run autonomous-fund backtest

research:
	uv run autonomous-fund research --config config/research.toml

paper:
	uv run autonomous-fund paper-run --config config/paper.toml
