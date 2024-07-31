# syntax=docker/dockerfile:1
FROM python:3.10-alpine
EXPOSE 8000
WORKDIR /code
COPY requirements.txt /code
RUN apk add bash
RUN apk add pkgconfig
RUN apk add mysql-client
RUN apk add musl-dev
RUN apk add gcc
RUN apk add mariadb-connector-c-dev
RUN pip install -r requirements.txt
COPY . /code
ENTRYPOINT [ "bash" ]
CMD [ "docker_entrypoint.sh" ]
