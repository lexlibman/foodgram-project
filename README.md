![foodgram-project](https://github.com/lexlibman/foodgram-project/workflows/foodgram/badge.svg)


# Foodgram


### Description
Foodgram is a site that lets you create your own recipes and share them with other people. 
You can also subscribe to recipe authors and add recipes to your shop-list 
and download the list with all ingredients you need.

The site is available on http://130.193.57.79


## Tech stack
- [Python 3.8.5](https://www.python.org/downloads/release/python-385/) <br>
- [Django 3.1.6](https://www.djangoproject.com) 
- [Django Rest Framework 3.12.2](https://www.django-rest-framework.org) <br>
- [Gunicorn 20.0.4](https://gunicorn.org) <br>
- [Nginx 1.19.6](https://www.nginx.com/resources/wiki/) <br>
- [PostgreSQL 13](https://www.postgresql.org) <br>
- [Docker](https://www.docker.com) <br>
- [Docker-Compose](https://docs.docker.com/compose/) <br>
- [GitHub Actions](https://github.com/features/actions) <br>
- [Yandex.Cloud](https://cloud.yandex.ru) <br>

## Setup
- Clone the github repository
    ```
    git clone https://github.com/lexlibman/foodgram-project.git
    ```
- Enter the project directory
    ```
    cd foodgram-project/
    ```
  
- Environment variables what you need are in `env.example` file. Put they to `.env` file and set yours values.
  

- Start docker-compose
    ```
    docker-compose up -d
    ```
  
- Start bash into container
    ```
    docker exec -it <CONTAINER ID> bash
    ```
  
#### Next commands will be executed in the container:
  
- Migrate to database
  ```
  python manage.py migrate
  ```
- Create superuser
    ```
    python manage.py createsuperuser
    ```
  
- Load test data
    ```
    python manage.py loaddata fixtures.json
    ```

## Authors

**Aleksei Libman** - *Initial work* - (https://github.com/lexlibman)

## Acknowledgments

Yandex.Praktikum