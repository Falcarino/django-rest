# syntax=docker/dockerfile:1
FROM python:3.8.10-alpine

COPY ./requirements.txt /tmp/requirements.txt
# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY ./entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

COPY ./api_handler /app

ENTRYPOINT ["/tmp/entrypoint.sh"]
