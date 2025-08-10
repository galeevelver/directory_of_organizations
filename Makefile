.PHONY: run up down reset migrate makemigrations seed lint format install freeze help

run:
	PYTHONPATH=src uvicorn src.main:app --reload

up:
	docker compose up --build -d

down:
	docker compose down -v

makemigrations:
	docker compose exec web alembic revision --autogenerate -m "init"

migrate:
	docker compose exec web alembic upgrade head

seed:
	docker compose exec web env PYTHONPATH=/app uv run python scripts/seed.py

reset:
	docker compose down -v
	find . -name '*.pyc' -delete
	rm -rf alembic/versions/*
	docker volume prune -f
	docker compose up --build -d
	sleep 3
	make makemigrations
	make migrate
	make seed

lint:
	ruff check src

lint-fix:
	ruff check src --fix

format:
	ruff format src

install:
	uv pip install -r requirements.txt

freeze:
	uv pip freeze > requirements.txt

help:
	@echo "Available commands:"
	@echo "  run              - Запустить приложение локально через uvicorn"
	@echo "  up               - Собрать и поднять контейнеры Docker"
	@echo "  down             - Остановить и удалить контейнеры и volume"
	@echo "  reset            - Полный сброс: очистка, миграции, сидинг"
	@echo "  makemigrations   - Сгенерировать миграцию Alembic"
	@echo "  migrate          - Применить миграции Alembic"
	@echo "  seed             - Наполнить БД тестовыми данными"
	@echo "  lint             - Проверка кода Ruff"
	@echo "  lint-fix         - Автоисправление Ruff"
	@echo "  format           - Форматирование кода Ruff"
	@echo "  install          - Установка зависимостей через uv"
	@echo "  freeze           - Экспорт зависимостей в requirements.txt"
