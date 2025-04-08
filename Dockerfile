FROM python:3.13.2

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app/app
COPY ./migrations /app/migrations
COPY alembic.ini /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]