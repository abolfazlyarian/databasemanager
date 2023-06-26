FROM python:3.10-slim

WORKDIR /usr/src/app

RUN pip install kubernetes
COPY database_manager.py .

CMD ["python", "database_manager.py"]
