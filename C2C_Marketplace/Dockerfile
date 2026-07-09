FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN set -e; \
    apt-get update ;\
    apt-get -y install netcat-openbsd ;\
    apt-get -y install gettext ;\
    /usr/local/bin/python -m pip install --upgrade pip ;\
    python -m pip install -r /app/requirements.txt ;\
    chmod +x /app/entrypoints/entrypoint.sh ;

EXPOSE 8000

ENTRYPOINT ["/app/entrypoints/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]