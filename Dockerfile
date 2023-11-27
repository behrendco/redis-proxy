FROM python:latest

WORKDIR /code

COPY ./requirements.txt /code
RUN pip3 install -r requirements.txt

COPY ./src /code/src
COPY ./tests/test_http /code/tests

CMD gunicorn -b ${PROXY_HOST}:${PROXY_PORT} -k gevent --worker-connections ${WORKER_CONNECTIONS} --chdir /code/src src.app:app