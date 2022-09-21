CREATE TABLE dht11(
time timestampz NOT NULL,
temperature DOUBLE PRECISION NOT NULL,
humidity DOUBLE PRECISION NOT NULL);

SELECT CREATE_hypertable('dht11', 'time');    #chunk_time_interval=7days