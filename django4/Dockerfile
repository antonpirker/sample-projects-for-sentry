
FROM python:3

#
# Build:
# docker build -t django4:v0 .
#
# Run:
# docker run --rm -p 8000:8000 -it django4:v0 
#


WORKDIR /app

COPY requirements.txt ./

RUN pip install -U pip && pip install -r requirements.txt

COPY movie_search/ .
COPY data/netflix_titles.csv .
COPY docker-entrypoint.sh docker-entrypoint.sh

RUN python ./manage.py collectstatic --clear --no-input && python ./manage.py migrate --no-input && python ./manage.py initadmin

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]

# You could use the same Docker image to run celery, by giving the celery command to your "docker run"
CMD ["gunicorn", "-b", "0.0.0.0:8000", "project.wsgi:application"]