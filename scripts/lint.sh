#!/bin/bash
set -e  # Exit on any error

# Change to the project root directory (where pyproject.toml is located)
cd "$(dirname "$0")/.."

echo "🧹 Running isort..."
uv run isort .

echo "⚫ Running black..."
uv run black .

echo "🔄 Running pyupgrade (PEP 604, etc.)..."
find . -name "*.py" -not -path "./.venv/*" -not -path "./.git/*" -exec uv run pyupgrade --py310-plus --exit-zero-even-if-changed {} \;

echo "🧽 Running autoflake (remove unused imports)..."
uv run autoflake --in-place --remove-all-unused-imports --recursive .

echo "🔍 Running flake8..."
uv run flake8 .

echo "✅ All formatting and linting complete!" 