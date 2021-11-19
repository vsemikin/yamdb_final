### Учебный проект Яндекс Практикум по работе с инфраструктурой разработки

В данном проекте не стояла задача написать сервис, сервис был готов ранее во время выполнения группового учебного проекта. Цель - изучить механизмы автоматизации разработки.

### Workflow статус:

![YaMDB workflow](https://github.com/vsemikin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### О проекте:

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).

### Docker для Ubuntu:

Инструкция по установке Docker:

https://docs.docker.com/engine/install/ubuntu/

### Клонировать образ проекта из Docker Hub:

Клонировать образ проекта на сервер:

```bash
docker pull vsemikin/yamdb
```
### Что должен содержать файл .env:

Файл .env содержит переменные окружения для работы с базой данных:

```yaml
DJANGO_SECRET_KEY # секретный ключ проекта
DJANGO_ALLOWED_HOSTS # список хостов для обслуживания проектом в формате: <host1, host2, host3>
DB_NAME # имя базы данных
POSTGRES_USER # логин для подключения к базе данных
POSTGRES_PASSWORD # пароль для подключения к БД
DB_HOST # название контейнера
DB_PORT # порт для подключения к БД
```

### Заполнение базы:

Сформировать файл json из начальных данных:

```bash
python manage.py dumpdata > fixtures.json
```

### Команды для docker:

Вход в контейнер:

```bash
docker exec -it <CONTAINER ID> bash
```

Запуск миграций:

```bash
docker-compose exec web python manage.py migrate --noinput
```

Запуск тестов:

```bash
docker-compose exec web pytest
```

Запустить проект:

```bash
docker-compose up
```

Остановка:

```bash
docker-compose stop
```

### Технологии проекта:

* Python
* Django
* PostgreSQL
* Docker
* NGINX
* GitHub

### Об авторе:

Семикин Владимир, студент 16 когорты факультета Бэкенд Яндекс Практикум.
