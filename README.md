# Installation

- `docker-compose up -d` => will launch kafka, zookeeper, grafana and influxdb.

## Kafka

Open 2 terminals:

- `python kafka/consumer.py` to consume messages
- `python kafka/producer.py` to send messages (coming from websocket crypto).

## Grafana

- `docker exec -ti influxdb bash` and create some data on influxdb (ex: `USE mydb` + `INSERT cpu,host=serverA,region=us_west value=0.64`)
- open [grafana dashboard](http://127.0.0.1:3000) and connect to influxdb. Credentials: admin/admin, user: 0.
