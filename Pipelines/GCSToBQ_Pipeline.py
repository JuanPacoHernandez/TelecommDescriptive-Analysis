import subprocess
from prefect import flow, task
from pyspark.sql import SparkSession


@task(log_prints=True, retries = 3)
def crm_from_gcs_to_bq():
    """Extracting crm dataset from GCS to ingesting into BigQuery as a external table"""
    try:
        print(subprocess.run(["./bash_scripts/crm_gcs_to_bq.sh"], shell=True))
        # NOTICE WHEN INGESTION FINISH
        print(f"\n\n< ---------- crm dataset from Bucket GCP was successfully transferred to the BigQuery, external table dbt_Analytics_Telecomm.external_CRM was created successfully ---------- >\n\n")
    except:
        print("******************** EXTERNAL TABLE COULDN'T BEEN CREATED ********************")
    return

@task(log_prints=True, retries = 3)
def dev_from_gcs_to_bq():
    """Extracting dev dataset from GCS to ingesting into BigQuery as a external table"""
    try:
        print(subprocess.run(["./bash_scripts/dev_gcs_to_bq.sh"], shell=True))
        # NOTICE WHEN INGESTION FINISH
        print(f"\n\n< ---------- dev dataset from Bucket GCP was successfully transferred to the BigQuery, external table dbt_Analytics_Telecomm.external_DEV was created successfully ---------- >\n\n")
    except:
        print("******************** EXTERNAL TABLE COULDN'T BEEN CREATED ********************")
    return

@task(log_prints=True, retries = 3)
def rev_from_gcs_to_bq():
    """Extracting rev dataset from GCS to ingesting into BigQuery as a external table"""
    try:
        print(subprocess.run(["./bash_scripts/rev_gcs_to_bq.sh"], shell=True))
        # NOTICE WHEN INGESTION FINISH
        print(f"\n\n< ---------- rev dataset from Bucket GCP was successfully transferred to the BigQuery, external table dbt_Analytics_Telecomm.external_REV was created successfully ---------- >\n\n")
    except:
        print("******************** EXTERNAL TABLE COULDN'T BEEN CREATED ********************")
    return
    
 
    
@flow()
def etl_gcs_to_bq():
    """MAIN ETL FLOW TO LOAD DATA INTO BIG QUERY"""
    crm_from_gcs_to_bq()
    dev_from_gcs_to_bq()
    rev_from_gcs_to_bq()    
         
if __name__ == '__main__':
    # MAIN FLOW
    etl_gcs_to_bq()




