# FastAPI project template

# Как использовать

## Настройка
1. Установи зависимости: `pip install -r requirements.txt`
2. Настрой pre-commit (для автоматического форматирования ruff-ом): `pre-commit install`
3. Скопируй .env.dist в .env: `cp .env.dist .env`
4. Подними все образы (в том числе postgres): `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build`

## Форматирование
Очень желательно выполнить пункт 2, чтобы один человек не переформатировал код другого.
Используется ruff (`ruff check --fix` и `ruff format`), список правил в pyproject.toml.
Если до чего-то сильно докапывается, бери код правила и добавляй в `ignore = [...]`

## Генерация миграций (после обновления моделей БД)
```shell
alembic revision --autogenerate -m "create account table"
```
База данных к этому моменту должна быть запущена

## Запуск/перезапуск сервера (со сборкой)
```shell
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up api -d --build
```
Отличие в том, что в этой команде собирается и перезапускается только образ `api`

## Запустить сервер без докера
В .env установи `DATABASE_URL=sqlite://db.sqlite3` и запускай `python3 -m uvicorn project:app --port=8080`.
В alembic.ini установи `sqlalchemy.url=sqlite://db.sqlite3` (теперь нужно следить за тем, чтобы не закоммитить его)

# Структура
- /app/deps/ - зависимости (`Depends(...)`) для переиспользования в /app/routes. 
Для каждой функции, которая является зависимостью, добавляем строку `MyFuncDep = Annotated[ReturnType, Depends(my_func)]`
(заменяя MyFunc и ReturnType) и используем в ручках как `value: MyFuncDep`
- /app/models/ - модели для SQLAlchemy.
Наследуемся от app.deps.database.Base, **которая уже содержит поля id, created_at и updated_at**
- /app/routes/ - ручки. Для каждого файла создаём свой роутер `router = APIRouter(tags=["Ping"])` 
и добавляем в `__init__.py` строку вида `app.include_router(ping.router)`.
Если лень, то объявляй роуты прямо на app, без роутеров
- /app/schemas/ - pydantic-модели для входных/выходных данных в ручках. 
Желательно наследоваться от `app.schemas.BaseSchema`.
Если модель используется для входных данных, можно добавить ограничения на значение поля при помощи Annotated
и чего-то из annotated_types. Примеры: `Annotated[int, Ge(0), Le(0]`,
`Annotated[str, StringConstraints(min_length=1)]`
- /app/asserts.py - можно использовать для дополнительной валидации данных.
В рамках хакатона нет смысла уточнять код ответа, просто кидаем 400

# Тесты

## Запуск тестов
```shell
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build --exit-code-from api --force-recreate
```
Запустит тесты внутри образа. База данных при каждом запуске - новая.