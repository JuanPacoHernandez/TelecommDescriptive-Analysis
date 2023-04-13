import subprocess
from pathlib import Path
from prefect import flow, task
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, lower

def createSparkSession():
    """This function creates  a Spark Session"""
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('SparkTelecomm') \
        .getOrCreate()
    # REMOVING SUCCESS FILE FROM THE OUTPUT
    spark.conf.set("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
    return spark
 

@task(log_prints=True, retries=3) 
def extract() -> None:
    """
    This function is the Extact Stage to fetch the dataset from URL, then will unzip the package in three files to proceed creating a DataFrame
    """
    # DOWNLOADING DATA USING BASH SCRIPT
    print(subprocess.run(["./bash_scripts/fetching_data.sh"], shell=True))
    return
    
@task(log_prints=True)
def clean_crm(spark) -> None:
    """
    This function will clean the crm1 dataset
    """
    # DEFINING THE SCHEMA FOR CRM
    crm_Schema=StructType([
                          StructField('msisdn', StringType(),nullable=True),
                          StructField('gender', StringType(),nullable=True),
                          StructField('year_of_birth', IntegerType(),nullable=True),
                          StructField('system_status', StringType(),nullable=True),
                          StructField('mobile_type', StringType(),nullable=True),
                          StructField('value_segment', StringType(),nullable=True)
                          ])
    # READING CSV DATASET
    crm_raw = spark.read \
        .option("header", "true") \
        .schema(crm_Schema) \
        .csv('data/crm1.csv')
    # CLEANSING CRM DATASET
        # To lowercase 'gender' col
    crm = crm_raw.withColumn('gender', lower(crm_raw['gender']))
        # The only two columns with Null values are year_of_birth and gender, removing Nulls in year_of_birth
        # represent less than 1% of the dataset but gender Nulls represent 20% of dataset, so this will be treated
        # as Not-Binaries
    crm = crm.filter(col('year_of_birth').isNotNull())
        # Filtering the dataset for Male, Female and Not-Binary (Null)
    crm = crm.filter("gender == 'male' or gender == 'female' or gender is NULL")
        # Replacing NULLs with 'Other'
    crm = crm.fillna('Other')
        # Filtering the dataset for users between 1943 and 2015 year of birth, the fact of using 1943 is 
        # the USA citizen's life expectancy is of 77 years in 2020 (the last record of life expectancy according 
        # to the World Bank), so these people should were born in 1943. The before 2015 records is for children with at least
        # 8 years and being smartphone users
    crm = crm.filter("year_of_birth >= 1943 and year_of_birth <= 2015")
    print("\n\n< ----------------- crm dataset has been cleansed successfully ---------------- >\n\n")
    return crm

@task(log_prints=True)
def clean_dev(spark) -> None:
    """
    This function will clean the device1 dataset
    """
    # DEFINING THE SCHEMA FOR DEV
    dev_Schema=StructType([
                          StructField('msisdn', StringType(),nullable=True),
                          StructField('imei_tac', StringType(),nullable=True),
                          StructField('brand_name', StringType(),nullable=True),
                          StructField('model_name', StringType(),nullable=True),
                          StructField('os_name', StringType(),nullable=True),
                          StructField('os_vendor', StringType(),nullable=True)
                          ])
    # READING CSV DATASET
    dev_raw = spark.read \
        .option("header", "true") \
        .schema(dev_Schema) \
        .csv('data/device1.csv')
    # CLEANSING DEV DATASET
        # Removing Null values at brand_name and model_name cols, these records represent the 1.2%, 
        # the other Null values are from os_name and os_vendor but they represent 27% of the dataset, then won't be removed
    dev = dev_raw.filter((col('brand_name').isNotNull() & col('model_name').isNotNull()))
    print("\n\n< ----------------- dev dataset has been cleansed successfully ---------------- >\n\n")
    return dev
    
@task(log_prints=True)
def clean_rev(spark) -> None:
    """
    This function will read the rev1 dataset
    """
    # DEFINING THE SCHEMA FOR REV
    rev_Schema=StructType([
                          StructField('msisdn', StringType(),nullable=True),
                          StructField('week_number', IntegerType(),nullable=True),
                          StructField('revenue_usd', FloatType(),nullable=True)
                          ])
    # READING CSV DATASET
    rev = spark.read \
        .option("header", "true") \
        .schema(rev_Schema) \
        .csv('data/rev1.csv')
    # CLEANSING REV DATASET
        # There is no need to clean rev dataset at this moment
    print("\n\n< ----------------- rev dataset has been cleansed successfully ---------------- >\n\n")
    return rev
    
@flow()
def main_flow() -> None: 
    """
    Main ETL Flow
    """
    # CREATING SPARK SESSION FOR BATCH PROCESSING
    spark = createSparkSession()

     # CREATING PARENT DIR TO STORE DATA IF NOT EXISTS
    path = Path(f"data/csv_gz")
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True)

    # ************************************** EXTRACT STAGE OF ALL DATASETS *********************************
    # ******************************************************************************************************
    extract()
  

    # ************************************** TRANSFORM STAGE ON CRM DATASET *********************************
    # *******************************************************************************************************
    # CLEAN STAGE FOR crm DATASET
    crm = clean_crm(spark)

    # WRITE DF OUT LOCALLY AS ONE CSV.GZ FILE
    crm.coalesce(1).write.mode("overwrite").option("compression", "gzip").csv("data/csv_gz/crm")

    
    # ************************************** TRANSFORM STAGE ON DEV DATASET *********************************
    # *******************************************************************************************************
    # CLEAN STAGE FOR dev DATASET
    dev = clean_dev(spark)

    # WRITE DF OUT LOCALLY AS ONE CSV.GZ FILE
    dev.coalesce(1).write.mode("overwrite").option("compression", "gzip").csv("data/csv_gz/dev")

    
    # ************************************** TRANSFORM STAGE ON REV DATASET *********************************
    # *******************************************************************************************************
    # CLEAN STAGE FOR rev DATASET
    rev = clean_rev(spark)

    # WRITE DF OUT LOCALLY AS ONE CSV.GZ FILE
    rev.coalesce(1).write.mode("overwrite").option("compression", "gzip").csv(f"{path}/rev")

    
    # ************************************** LOAD STAGE OF ALL DATASETS *************************************
    # *******************************************************************************************************
    # UPLOADING ALL THREE DATASETS TO GCS BUCKET USING BASH SCRIPT
    print(subprocess.run(["./bash_scripts/uploading_data.sh"], shell=True))
    
if __name__ == "__main__":
    """MAIN ETL FLOW TO FETCH DATA FROM URL TO INGEST INTO GCS CLOUD STORAGE"""
    main_flow()
