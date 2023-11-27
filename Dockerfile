FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock src .env ./

RUN pip3 install --upgrade pip
RUN pip3 install poetry --no-cache-dir
RUN poetry config virtualenvs.create false && poetry install --no-root --no-directory --no-dev --no-interaction --no-ansi

CMD ["python3", "bot.py"]
