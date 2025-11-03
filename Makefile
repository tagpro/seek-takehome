.phony: install
install:
	uv sync

.phony: lint
lint:
	uv run ruff check .
	uv run mypy src

.phony: lint-fix
lint-fix:
	uv run ruff check . --fix
	uv run mypy src --fix

.phony: format
format:
	uv run ruff format .

.phony: test
test:
	uv run pytest tests/ --ignore=tests/integration/

.phony: test-integration
test-integration:
	# runs only integration tests
	uv run pytest tests/integration/


