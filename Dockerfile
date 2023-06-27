FROM python:3.10-slim

WORKDIR /usr/src/app
RUN apt-get update \
    && apt-get install -y libpq-dev

RUN pip install psycopg2-binary
RUN pip install kubernetes
#RUN pip install -r requirements.txt

COPY *.py .

CMD ["python", "database_manager.py"]
