# Expense Tracker API

A small FastAPI service for tracking expenses: categorizing them, summarizing monthly totals, checking budgets and converting currencies. Built test-first as a practice project.

## Setup

Requires Python 3.11 or newer.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running the tests

```bash
pytest
```

## Project layout

```
expense_tracker/   application code
tests/unit/        fast tests for pure logic
tests/integration/ tests for the database and API
```
