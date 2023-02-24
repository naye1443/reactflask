FROM python:3.10.10 as build

WORKDIR /app

COPY flask-server/ /app/
RUN pip install -r requirements.txt
CMD ["python", "server.py"]
EXPOSE 80