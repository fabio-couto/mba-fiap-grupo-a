from pyspark.sql import SparkSession
from hdfs import Client
from datetime import datetime
import os

hdfs = Client('http://namenode:50070')
spark = SparkSession.builder.getOrCreate()

TRANSIENT_PATH = "/datalake/transient/machines"
RAW_PATH = "/datalake/raw/machines"
DW_PATH = "/datalake/datawarehouse/machines"

def process_file(file_name):
    transient_file_path = TRANSIENT_PATH + "/" + file_name
    name, ext = os.path.splitext(transient_file_path)
    name = os.path.basename(name)
    raw_file_path = RAW_PATH + "/" + "{name}.{timestamp}{ext}".format(name=name, timestamp=datetime.today().strftime('%Y%m%d%H%M%S'), ext=ext)
    
    if exists_data_dw():
        import_with_scd_type2(transient_file_path)
    else:
        first_import(transient_file_path)

    hdfs.makedirs(RAW_PATH)
    hdfs.rename(transient_file_path, raw_file_path)

def first_import(file_path):
    spark.read.csv(file_path, header=True).createOrReplaceTempView("vw_incoming")
    spark.sql("""
        SELECT
            ROW_NUMBER() OVER (ORDER BY int(i.machineID)) AS machineSK,
            int(i.machineID) AS machineID,
            i.model,
            int(i.age) as age,
            current_timestamp() AS startDate,
            timestamp('9999-12-31') AS endDate,
            true AS isCurrent,
            1 AS version
        FROM vw_incoming i
    """).write.parquet(DW_PATH, mode="overwrite")

def import_with_scd_type2(file_path):
    spark.read.csv(file_path, header=True).createOrReplaceTempView("vw_incoming")
    spark.read.parquet(DW_PATH).createOrReplaceTempView("vw_dw")
    
    # Apura quais registros sofreram alteração
    spark.sql("""
        SELECT changed_records.machineID, dw.version, current_timestamp() timestamp, false AS isCurrent
        FROM (
            SELECT records.machineID
            FROM (
                SELECT 
                    c.machineID,
                    c.model,
                    c.age
                FROM vw_dw c
                WHERE c.isCurrent = true
                UNION
                SELECT
                    int(i.machineID),
                    i.model,
                    int(i.age)
                FROM vw_incoming i
            ) records
            GROUP BY records.machineID
            HAVING COUNT(*) > 1
        ) changed_records
        INNER JOIN vw_dw dw ON changed_records.machineID = dw.machineID AND dw.isCurrent = true
    """).createOrReplaceTempView("vw_changes")

    # Gera nova visão
    df = spark.sql("""
        SELECT
            c.machineSK,
            c.machineID,
            c.model,
            c.age,
            c.startDate,
            COALESCE(h.timestamp, c.endDate) AS endDate,
            COALESCE(h.isCurrent, c.isCurrent) AS isCurrent,
            c.version
        FROM vw_dw c
        LEFT JOIN vw_changes h ON h.machineID = c.machineID AND h.version = c.version
        UNION ALL
        SELECT
            (SELECT MAX(machineSK) FROM vw_dw) + ROW_NUMBER() OVER (ORDER BY int(i.machineID)) AS machineSK,
            int(i.machineID) AS machineID,
            i.model,
            int(i.age) as age,
            h.timestamp AS startDate,
            timestamp('9999-12-31') AS endDate,
            true AS isCurrent,
            h.version + 1 AS version
        FROM vw_incoming i
        INNER JOIN vw_changes h ON h.machineID = i.machineID
    """).cache()

    print("Count: " + str(df.count()))
    
    df.write.parquet(DW_PATH, mode="overwrite")

def exists_data_dw():
    if hdfs.status(DW_PATH, strict=False) == None:
        return False

    if len(hdfs.list(DW_PATH)) == 0:
        return False

    return True

def main():
    for file in hdfs.list(TRANSIENT_PATH):
        print('Starting processing file ' + file)
        process_file(file)

    print('Execution finished')

main()