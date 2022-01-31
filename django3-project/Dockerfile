FROM python:3

ARG IS_WUNDERPREVIEW
ENV IS_WUNDERPREVIEW = $IS_WUNDERPREVIEW

WORKDIR /app

COPY demosite/requirements.txt ./

RUN pip install -U pip && pip install -r requirements.txt

COPY demosite/ .
COPY data/pokemon.csv .
COPY docker-entrypoint.sh docker-entrypoint.sh

RUN python ./manage.py collectstatic --clear --no-input && python ./manage.py migrate --no-input && python ./manage.py initadmin

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]

# You could use the same Docker image to run celery, by giving the celery command to your "docker run"
CMD ["gunicorn", "-b", "0.0.0.0:8000", "demosite.wsgi:application"]
