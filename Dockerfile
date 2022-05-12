FROM python:3.8.10-alpine

LABEL Maintainer="Kevin Ogaba"

# set working directory
RUN mkdir /app
WORKDIR /app

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFED 1

# dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .