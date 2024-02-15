# QRkot_spreadseets
Учебный проект: API приложения для Благотворительного фонда поддержки котиков QRKot.
Его назначение — сбор и распределение пожертвований между различными проектами и формирование отчетов о времени закрытия проектов
в гугл таблицах


## Технологии и библиотеки

 - Python 3.7
 - FastAPI (веб-фреймворк для создания API)
 - SQLAlchemy (библиотека для работы с реляционными СУБД с применением технологии ORM)
 - Pydantic (библиотека для валидации и сериализации данных)
 - Alembic (инструмент для миграции базы данных)
 - Uvicorn (высокопроизводительный ASGI сервер)
 - Google Cloud Platform
 - Google Sheets API
 - Google Drive API

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Nikitkosss/QRkot_spreadsheets.git
```
```
cd QRkot_spreadsheets
```
Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Примените миграции:
```
alembic upgrade head
```
Запустить проект:
```
uvicorn app.main:app --reload
```

## API
Документация и web интервейс API будет доступен по адресу: http://localhost:8000/docs

## Автор проекта

[Пискунов Никита](https://github.com/Nikitkosss)