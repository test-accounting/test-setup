FROM python:3.8.10-alpine

LABEL Maintainer="Kevin Ogaba"

# set working directory
RUN mkdir /app
WORKDIR /app/

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev 

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFED 1

# dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# copy project
COPY . /app/

# RUN entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]