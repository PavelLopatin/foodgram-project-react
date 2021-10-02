FROM python:3.8

WORKDIR /code
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r /code/requirements.txt --no-cache-dir
COPY . .
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000