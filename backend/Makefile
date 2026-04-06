.PHONY: install migrate run worker test

PYTHON_LOCAL := .venv/bin/python
PYTHON_ROOT := ../.venv/bin/python
ifeq ($(wildcard $(PYTHON_LOCAL)),)
PYTHON := $(PYTHON_ROOT)
else
PYTHON := $(PYTHON_LOCAL)
endif

install:
	python3 -m venv .venv
	$(PYTHON_LOCAL) -m pip install -r requirements.txt

migrate:
	$(PYTHON) -m alembic upgrade head

run:
	$(PYTHON) -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

worker:
	$(PYTHON) -m celery -A app.worker.celery_app.celery_app worker --loglevel=info

test:
	$(PYTHON) -m pytest -q
