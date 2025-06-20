#!/bin/bash
set -e  # Exit on any error

echo "🧹 Running isort..."
isort .

echo "⚫ Running black..."
black .

echo "🔧 Running ruff fix (auto-fixable issues)..."
ruff check . --fix

echo "🔍 Running ruff check (configured rules)..."
ruff check .

echo "✅ All formatting and linting complete!" 