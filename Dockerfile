FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt *.py .env ./
COPY tg_handlers ./tg_handlers

RUN pip3 install --upgrade pip
RUN pip3 install -r  /app/requirements.txt --no-cache-dir

RUN apt update && apt install -y cron

RUN crontab -l | { cat; echo "0 12,18 * * * python3 /app/cron.py"; } | crontab -

CMD ["python3", "birthdaygram.py"]