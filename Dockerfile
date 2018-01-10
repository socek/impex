FROM python:3.6.2

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /code
WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR
RUN pip install -r requirements.txt --no-cache-dir

COPY . $APP_DIR
RUN python setup.py develop
RUN mkdir data
CMD uwsgi --ini-paste frontend.ini

EXPOSE 8000

