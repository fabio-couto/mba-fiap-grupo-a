from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, from_unixtime, to_date, to_timestamp
from pyspark.sql.types import BooleanType, FloatType, IntegerType, StringType, StructField, StructType, TimestampType
from pyspark.storagelevel import StorageLevel

spark = SparkSession.builder.getOrCreate()

#pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.2.3

jsonSchema = StructType([
    StructField("timestamp", FloatType()),
    StructField("medida", StringType()),
    StructField("machineID", IntegerType()),
    StructField("value", FloatType()),
])

machineParquetSchema = StructType([
    StructField("machineSK", IntegerType()),
    StructField("machineID", IntegerType()),
    StructField("model", StringType()),
    StructField("age", IntegerType()),
    StructField("startDate", TimestampType()),
    StructField("endDate", TimestampType()),
    StructField("isCurrent", BooleanType()),
    StructField("version", IntegerType())
])

#Criação dos DataFrames
machines = spark.read \
            .schema(machineParquetSchema) \
            .parquet("/datalake/datawarehouse/machines") \
            .filter("isCurrent = true") \
            .select('machineID', 'machineSK') \
            .persist(StorageLevel.MEMORY_ONLY)

telemetry = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "kafka:29092") \
            .option("subscribe", "iot-telemetry") \
            .load() \
            .selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", jsonSchema).alias("json")) \
            .select("json.*") \
            .join(machines, "machineID") \
            .withColumn("datetime", to_timestamp(from_unixtime("timestamp"))) \
            .withColumn("dateSK", to_date(from_unixtime("timestamp"))) \
            .withColumnRenamed("medida", "metric") \
            .select("datetime", "machineSK", "dateSK", "metric", "value")

telemetry \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/datalake/datawarehouse/telemetry") \
    .option("checkpointLocation", "/checkpoint") \
    .start() \
    .awaitTermination()