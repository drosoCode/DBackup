FROM python:3

WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y tzdata default-mysql-client postgresql-client wget && \
    wget https://dl.influxdata.com/influxdb/releases/influxdb_1.8.5_amd64.deb && dpkg -i influxdb_1.8.5_amd64.deb && rm influxdb_1.8.5_amd64.deb && \
    wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian10-x86_64-100.3.1.deb && dpkg -i mongodb-database-tools-debian10-x86_64-100.3.1.deb && rm mongodb-database-tools-debian10-x86_64-100.3.1.deb && \
    pip3 install -r requirements.txt
COPY . .
RUN chmod +x main.py

CMD ["/app/main.py"]