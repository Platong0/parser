FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TZ=Europe/Madrid

RUN echo "0 12 * * * cd /app && /usr/local/bin/python3 parser.py >> /var/log/parser.log 2>&1" | crontab -

CMD ["cron", "-f"]
