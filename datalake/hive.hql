create database if not exists dw_usina
location '/datalake/datawarehouse';

CREATE EXTERNAL TABLE IF NOT EXISTS DIM_MACHINE (
    machineSK INT,
    machineID INT,
    model STRING,
    age INT,
    startDate TIMESTAMP,
    endDate TIMESTAMP,
    isCurrent BOOLEAN,
    version INT
)
STORED AS PARQUET
LOCATION '/datalake/datawarehouse/machines';

CREATE EXTERNAL TABLE IF NOT EXISTS TELEMETRY (
    datetime TIMESTAMP,
    machineSK INT,
    dateSK DATE,
    metric STRING,
    value FLOAT
)
STORED AS PARQUET
LOCATION '/datalake/datawarehouse/telemetry';