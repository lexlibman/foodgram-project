FROM python:3.8

WORKDIR /code

COPY requirements.txt .

COPY . .

RUN python3 -m pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 --access-logfile