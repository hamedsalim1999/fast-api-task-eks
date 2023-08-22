
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS builder

COPY . /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /app

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]