# Foodgram


![foodgram-project](https://github.com/lexlibman/foodgram-project/workflows/foodgram/badge.svg)


### Description
Foodgram is a site that lets you create your own recipes and share them with other people. You can also subscribe to recipe authors and add recipes to your shop-list - 
and download the list with all ingredients you need.

The site is available on http://130.193.57.79


## Tech stack
- Python 3.8
- Django and Django Rest Framework
- PostgreSQL
- Gunicorn + Nginx
- CI/CD: Docker, docker-compose, GitHub Actions
- Yandex.Cloud

## Setup
- Clone the github repository
    ```
    git clone https://github.com/lexlibman/foodgram-project.git
    ```
- Enter the project directory
    ```
    cd foodgram-project/
    ```
- Start docker-compose
    ```
    docker-compose -f docker-compose.yaml up -d
    ```
- Create superuser
    ```
    docker-compose -f docker-compose.yaml run --rm foodgram python manage.py createsuperuser
    ```
### Optional
- Load test data
    ```
    docker-compose -f docker-compose.yaml run --rm foodgram python manage.py loaddata fixtures.json
    ```
