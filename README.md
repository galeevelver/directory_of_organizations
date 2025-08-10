# Directory of Organizations — API

REST API для справочника организаций, зданий и видов деятельности.

## Клонирование проекта
```bash
git clone https://github.com/galeevelver/directory_of_organizations.git
cd directory_of_organizations
```
## Развёртывание проекта
Создать `.env` на основе шаблона:
```bash
cp .env.example .env
```

### С Docker + Make
```bash
make up       # сборка и запуск контейнеров
make migrate  # применить миграции
make seed     # наполнить базу тестовыми данными
```
Или:
```bash
make reset    # очистка и полный перезапуск с сидингом
```
Удалить все запущенные контейнеры и volumes:
```bash
make down
```

### Без Make

```bash
docker-compose up --build -d
docker-compose exec web alembic upgrade head
docker-compose exec web env PYTHONPATH=/app uv run python scripts/seed.py
```

## Swagger UI

Доступно по адресу: [http://localhost:8000/docs]

### Примеры запросов в курле
```bash
curl -G http://127.0.0.1:8000/organizations/search --data-urlencode "query=ОМК"
curl -G http://127.0.0.1:8000/organizations/geo \
  --data-urlencode "lat=11.36" \
  --data-urlencode "lon=151.66" \
  --data-urlencode "radius_km=1"
curl -G http://127.0.0.1:8000/organizations/geo \
  --data-urlencode "min_lat=11.35" \
  --data-urlencode "max_lat=11.37" \
  --data-urlencode "min_lon=151.64" \
  --data-urlencode "max_lon=151.67"
curl http://127.0.0.1:8000/organizations/activity/4
curl http://127.0.0.1:8000/organizations/building/1
curl http://127.0.0.1:8000/organizations/3
curl http://127.0.0.1:8000/buildings
curl http://127.0.0.1:8000/activities
```


## Тестовые данные из сидера
* Виды деятельности (ID):
  `1: Еда`, `2: Автомобили`
  `3: Мясная`, `4: Молочная`, `5: Грузовые`, `6: Легковые`, `7: Аксессуары`, `8: Запчасти`
* Организации:
  `1: ОМК` (гарантированно есть)
* Здания:
  5 штук, координаты вблизи `11.36, 151.66` (чтобы прошел geo)
* У каждой организации:
  2 телефона и 2 направления деятельности.