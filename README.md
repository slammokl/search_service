markdown
# Posts Search Service

Простой поисковик по текстам документов.
- **PostgreSQL** — хранит документы (id, text, rubrics, created_date).
- **Elasticsearch** — хранит поисковый индекс (id, text).
- **FastAPI** — HTTP-API.

## Эндпоинты

GET `/search?q=<query>` - поиск по тексту, возвращает 20 документов по убыванию даты 
DELETE `/documents/{doc_id}` - удаляет документ из БД и индекса 
GET `/docs` - Swagger 
GET `/openapi.json` - OpenAPI-схема 

## Запуск

### 1. Поднять инфраструктуру

```bash
docker compose up -d
```

Дождитесь, пока Elasticsearch станет доступен:

```bash
curl http://localhost:9200
```

### 2. Установить зависимости

```bash
python -m venv .project
source .project/bin/activate      
pip install -r requirements.txt
```

### 3. Настроить окружение

```bash
cp .env.example .env
```

### 4. Загрузить данные из posts.csv

```bash
python -m scripts.load_data posts.csv
```

### 5. Запустить сервис

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Примеры запросов

```bash
# поиск
curl "http://localhost:8000/search?q=fastapi"

# удаление
curl -X DELETE "http://localhost:8000/documents/1"
```

## Генерация docs.json

```bash
curl -s http://localhost:8000/openapi.json > docs.json
```

## Остановка

```bash
docker compose down
# с удалением томов:
docker compose down -v
```