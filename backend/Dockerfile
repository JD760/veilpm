FROM python:3.14-alpine

RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    libpq \
    gcc \
    musl-dev \
    python3-dev \
    linux-headers

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./src /app/src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
