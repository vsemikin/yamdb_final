![YaMDB workflow](https://github.com/vsemikin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### О проекте:

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).

### Docker для Ubuntu:

Инструкция по установке Docker:

```
https://docs.docker.com/engine/install/ubuntu/
```

### Клонировать образ проекта из Docker Hub:

Клонировать образ проекта на сервер:

```docker
docker pull vsemikin/yamdb
```
### Что должен содержать файл .env:

Файл .env содержит переменные окружения для работы с базой данных:

```yaml
DJANGO_SECRET_KEY # секретный ключ проекта
DJANGO_DEBUG # активировать/деактивировать режим разработчика
DJANGO_ALLOWED_HOSTS # список хостов для обслуживания проектом
DB_NAME # имя базы данных
POSTGRES_USER # логин для подключения к базе данных
POSTGRES_PASSWORD # пароль для подключения к БД
DB_HOST # название контейнера
DB_PORT # порт для подключения к БД
```
### Команды для docker:

Вход в контейнер:

```docker
docker exec -it <CONTAINER ID> bash
```

Запуск миграций:

```docker
docker-compose exec web python manage.py migrate --noinput
```

Запуск тестов:

```docker
docker-compose exec web pytest
```

Остановка:

```docker
docker-compose stop
```

### Технологии проекта:

Python
Django
PostgreSQL
Docker
NGINX
GitHub

### Об авторе:

Семикин Владимир, студент 16 когорты факультета Бэкенд Яндекс Практикум.

### Проект:

http://178.154.240.96/