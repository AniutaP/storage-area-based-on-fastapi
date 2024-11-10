FROM python:3.12

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN apt-get update && apt-get install -y postgresql-client

COPY . .

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]