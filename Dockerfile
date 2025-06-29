FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir playwright
RUN playwright install --with-deps chromium

RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*

COPY . .

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]