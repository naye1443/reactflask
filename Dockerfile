FROM python:3.10.10 as build

WORKDIR /app

COPY . /app/

WORKDIR /app/flask-server

RUN pip install -r requirements.txt

CMD ["python", "server.py"]
EXPOSE 80