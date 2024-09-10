FROM python:3.11-slim
LABEL authors="yagorezende"

RUN apt-get update \
 && apt-get install -y gcc=4:12.2.0-3 vim=2:9.0.1378-2 --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]