FROM python:3.9-alpine3.15

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . ./

CMD exec python main.py