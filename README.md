# Blog_FastAPI

## Описание

API для блога с юзерами, постами и лайками.

## Технологии

FastAPI, PostgreSQL, SQLAlchemy, fastapi_users, docker, alembic

## Как запустить

Создать .env файл в корне проекта вида:

```env
DB_USER=postgres
DB_PASS=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=postgres
TOKEN_SECRET_KEY=<секретный ключ для токена(любой)>
USER_SECRET_KEY=<секретный ключ для юзеров(любой)
EMAIL_API = <ваш API ключ для EmailHunter>
```

Из корневой директории запустить docker-compose

```bash
docker-compose up -d
```

Документация Swagger будет доступна по адресу <http://0.0.0.0:8000/docs>.
