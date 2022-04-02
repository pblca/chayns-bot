FROM python:3.9-alpine3.15

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN apk add git
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del git #lel

CMD exec python main.py