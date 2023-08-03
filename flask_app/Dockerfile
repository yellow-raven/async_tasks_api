FROM python:3.9-buster

WORKDIR /flask_app

COPY . /flask_app
RUN pip3 --no-cache-dir install -r requirements.txt

ENV FLASK_ENV=development
EXPOSE 5001

CMD ["python","app.py", "--loglevel=info"]

#CMD gunicorn --workers $WORKERS \
#  --threads $THREADS \
#  --bind 0.0.0.0:$PORT_APP \
#  --log-level DEBUG \
#  app:app