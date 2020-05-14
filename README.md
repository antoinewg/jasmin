# Installation

- `docker-compose up -d` => will launch kafka, zookeeper, grafana and influxdb.

## Kafka

Open 2 terminals:

- `python kafka/consumer.py` to consume messages
- `python kafka/producer.py` to send messages (coming from websocket crypto).

## Grafana

- `docker exec -ti influxdb bash` and create some data on influxdb (ex: `USE mydb` + `INSERT cpu,host=serverA,region=us_west value=0.64`)
- open [grafana dashboard](http://127.0.0.1:3000) and connect to influxdb. Credentials: admin/admin, user: 0.

## Management Commands

- `heroku run python manage.py detect_gaps [--from=D] [--exchange=US/PA/...]`

> - from: letter(s) to start from. Ex: `--from=MSFT`
> - exchange: exchange to check symbols from. Ex: `--exchange=PA`
