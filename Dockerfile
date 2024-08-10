FROM python:3.9.14

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libgl1\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN git config --global --add safe.directory /app

RUN pip install poetry \
  && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install

WORKDIR /usr/flask_api/

COPY ./__init__.py /usr/flask_api/__init__.py
COPY ./api /usr/flask_api/api
COPY ./model.pt /usr/flask_api/model.pt
COPY ./run.py /usr/flask_api/run.py

RUN echo "building..."

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
