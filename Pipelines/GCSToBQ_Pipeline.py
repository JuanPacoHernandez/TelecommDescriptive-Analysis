import subprocess
from prefect import flow, task
from pyspark.sql import SparkSession
import logging
logger = logging.getLogger(__name__)


@task(log_prints=True, retries = 3)
def extract_crm_from_gcs_to_bq(script_path: str):
    """Extracting crm dataset from GCS to ingesting into BigQuery as a external table"""
    try:
        # NOTICE WHEN EXTRACTION STAGE START
        logger.info("Starting extract_crm_from_gcs_to_bq")
        subprocess.run([script_path], shell=True, check=True)
        # NOTICE WHEN INGESTION FINISH
        logger.info("crm dataset from Bucket GCP was successfully transferred to the BigQuery, external table dbt_Analytics_Telecomm.external_CRM was created successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error:{e}")
        raise Exception("EXTERNAL TABLE COULDN'T BEEN CREATED")
    return

@task(log_prints=True, retries = 3)
def extract_dev_from_gcs_to_bq(script_path: str):
    """Extracting dev dataset from GCS to ingesting into BigQuery as a external table"""
    try:
        # NOTICE WHEN EXTRACTION STAGE START
        logger.info("Starting extract_dev_from_gcs_to_bq")
        subprocess.run([script_path], shell=True, check=True)
        # NOTICE WHEN INGESTION FINISH
        logger.info("dev dataset from Bucket GCP was successfully transferred to the BigQuery, external table dbt_Analytics_Telecomm.external_DEV was created successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error:{e}")
        raise Exception("EXTERNAL TABLE COULDN'T BEEN CREATED")
    return

@task(log_prints=True, retries = 3)
def extract_rev_from_gcs_to_bq(script_path: str):
    """Extracting rev dataset from GCS to ingesting into BigQuery as a external table"""
    try:
        # NOTICE WHEN EXTRACTION STAGE START
        logger.info("Starting extract_rev_from_gcs_to_bq")
        subprocess.run([script_path], shell=True, check=True)
        # NOTICE WHEN INGESTION FINISH
        logger.info("rev dataset from Bucket GCP was successfully transferred to the BigQuery, external table dbt_Analytics_Telecomm.external_REV was created successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error:{e}")
        raise Exception("EXTERNAL TABLE COULDN'T BEEN CREATED")
    return
    
 
    
@flow()
def etl_gcs_to_bq():
    """MAIN ETL FLOW TO LOAD DATA INTO BIG QUERY"""
    crm_script_path = "./bash_scripts/crm_gcs_to_bq.sh"
    dev_script_path = "./bash_scripts/dev_gcs_to_bq.sh"
    rev_script_path = "./bash_scripts/rev_gcs_to_bq.sh"
    extract_crm_from_gcs_to_bq(crm_script_path)
    extract_dev_from_gcs_to_bq(dev_script_path)
    extract_rev_from_gcs_to_bq(rev_script_path)    
         
if __name__ == '__main__':
    # MAIN FLOW
    etl_gcs_to_bq()




