FROM python:3.11-alpine
LABEL maintainer="avburmistrov@mail.ru"

EXPOSE 8000

COPY ./deploy/python/requirements.txt /
RUN pip install -r requirements.txt --no-cache-dir

COPY ./src /app
WORKDIR /app

CMD ["uvicorn"  , "--host", "0.0.0.0", "--port", "8000", "main:app"]
