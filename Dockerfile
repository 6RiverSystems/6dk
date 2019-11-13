FROM python:3.6

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["/app/entrypoint.sh"]

RUN wget -q -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64  &&\
    rm -rf /tmp/*.tar.gz &&\
    chmod +x /usr/local/bin/dumb-init 

RUN  apt-get update && apt-get install -y nginx
COPY docker-deps/nginx.conf /etc/nginx/nginx.conf
COPY docker-deps/entrypoint.sh /app/entrypoint.sh

RUN pip install pipenv

RUN groupadd -g 999 appuser && \
    useradd -r -m -u 999 -g appuser appuser
# USER appuser

ENV FLASK_APP=6dk.py

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

WORKDIR /app

RUN pipenv install

COPY --chown=appuser:appuser . /app/