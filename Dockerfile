FROM python:3.9

RUN pip install Flask Flask-JWT-Extended Werkzeug

COPY . /app
WORKDIR /app

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run"]
