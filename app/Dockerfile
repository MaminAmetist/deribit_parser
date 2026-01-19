version: "3.9"

services:
  api:
    build: .
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"

  worker:
    build: .
    command: celery -A celery_worker worker -B
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: prices
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

  redis:
    image: redis:7
