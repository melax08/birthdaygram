FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt src ./

RUN pip3 install --upgrade pip
RUN pip3 install poetry --no-cache-dir
RUN poetry install

CMD ["python3", "bot.py"]