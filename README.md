# yamdb_final
# Сверхинновационное приложение api_yamdb

## Описание
Сверхнновационное приложение, социальная сеть для любителей творчества, позволяющее создавать рецензии на художественные произведения и ставлять комментарии на них.

## Как развернуть проект на локальной машине:

- Клонируем репозиторий:

```git clone https://github.com/Arhifant/yamdb_final.git```

- Переходим в папку инфраструктуры проекта:

```cd yamdb_final/infra```

- Открываем файл .env.sample и меняем необходимые параметры:
```nano .env.sample```

- Переименовываем файл:
```mv .env.sample .env```

- Собираем образ и запускаем контейнеры:

```docker-compose up -d```

- Применяем миграции, создаем суперпользователя и собираем статику:

```docker-compose exec web python manage.py migrate```

```docker-compose exec web python manage.py createsuperuser``` 

```docker-compose exec web python manage.py collectstatic --no-input``` 

Документация при локальном запуске доступна по адресу: 
```127.0.0.1:8000/redoc/```

## Примеры запросов
GET ```http://158.160.25.80/api/v1/categories/``` - получение списка категорий

Данные на выходе:  

```
{  
  "name": "string",  
  "slug": "string"  
}
```  

POST ```http://158.160.25.80/api/v1/titles/{title_id}/reviews/``` -добавление нового отзыва

Данные на входе:
```  
{  
  "text": "string",  
  "score": 1  
}  
```

## Статус workflow:

![Yamdb workflow](https://github.com/Arhifant/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Дополнительно

Проект доступен по адресу: 

```http://158.160.25.80```

Документация API доступна по адресу:

```http://158.160.25.80//redoc/```

## Использованные технологии

Django REST Framework 3.12.4
