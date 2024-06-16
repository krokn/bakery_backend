FROM python:3.12

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN echo "Checking alembic version"

RUN alembic current

RUN alembic upgrade 4b182af28f83

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000