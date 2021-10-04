# FOODGRAM PROJECT - [«Продуктовый помощник»](http://www.myrecipesfoodgram.ga/).
____
[![Build Status](https://travis-ci.com/h0diush/foodgram-project-react.svg?branch=master)](https://travis-ci.com/h0diush/foodgram-project-react)

## Описание
Дипломный проект — сайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. 
На этом сервисе пользователи можно публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин 
скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

- В папке *frontend* находятся файлы, необходимые для сборки фронтенда приложения.
- В папке *infra* — заготовка инфраструктуры проекта: конфигурационный файл nginx и docker-compose.yml.
- В папке *backend* API сервис на _DRF_, _Djoser_, _Django_.
- В папке *docs* — файлы спецификации API.


## Инфраструктура

- Проект работает с СУБД PostgreSQL.
- Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. Контейнер с проектом обновляется на Docker Hub
- В nginx настроена раздача статики, остальные запросы переадресуются в Gunicorn.
- Данные сохраняются в volumes.
- Код соответствует PEP8.


### Установка Для работы с проектом необходимо установить Docker: https://docs.docker.com/engine/install/

Клонируйте репозиторий к себе на сервер командой:
```
git clone https://github.com/wildd1994/foodgram-project-react .
```
В корне проекта создайте файл .evn и заполните его:
```
POSTGRES_NAME=postgres  # имя базы postgres<br/>
POSTGRES_USER=postgres # имя пользователя postgres<br/>
POSTGRES_PASSWORD=postgres # пароль для базы postgres<br/>
DB_HOST=postgresql   #имя хоста базы данных<br/>
DB_PORT=5432  #порт<br/>
```
Перейдите в каталог infra и запустите создание контейнеров:
```
docker-compose up -d --build
```
Первоначальная настройка проекта:
```
docker-compose exec web foodgram/python manage.py migrate --noinput
docker-compose exec web foodgram/python manage.py collectstatic --no-input
```
Создание суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
Загрузка фикстур
```
docker exec backend python manage.py loaddata fixtures.json
```
После сборки, проект будет доступен по имени хоста вашей машины, на которой был развернут проект.
Проект доступен по адресу http://84.201.157.75/admin
### Вход на сайт/в админку:
```
lopatyn1244@gmail.com
lopatyn1244s
```