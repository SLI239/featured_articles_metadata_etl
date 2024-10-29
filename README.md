# ETL Pipeline for Creating a Catalog of Featured Articles on AWS
This Airflow pipeline has been developed to collect metadata of featured articles from Wikipedia, for creating a data lake on AWS. It 1) fetches metadata of daily featured articles from Wikimedia, 2) filters and cleans the dataset and 3) uploads the dataset to S3 and triggers AWS Glue crawler. It creates/updates the Glue data catalog on a daily basis, and you can easily query the catalog using AWS Athena. The future goal of this project is to build a basis of a collective article collection on AWS, by adding more data sources.


## Prerequisite
1.  **Wikimedia Cliend Id and Client Secret**\
  Take a look at [Getting started with Wikimedia APIs](https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs)
2.  **AWS Stack**\
  Create an S3 bucket and Glue Crawler using AWS the Cloud Formation Template (aws_create_stack.yaml). Make sure that the name of the S3 bucket is *articles-metadata-bucket*
3.  **Docker Desktop**\
  Installation guide on the official website is [here](https://docs.docker.com/compose/install/)
   

## How to Run
1. Git clone and Set up directory structure
```
git clone 
```

# 1. BUILD DOCKER IMAGE WITH PYTHON PACKAGES NEEDED
# FIRST CREATE DIRECTORIES
mkdir ./config ./data ./logs ./plugins
docker build --build-arg AIRFLOW_VERSION=2.10.2 -t apache/airflow-custom:2.10.2 .

# 2. CREATE .env AND RUN DOCKER COMPOSE
docker-compose up

# 3. SET UP CONNECTIONS AND VARIABLES ON THE WEB UI
WIKI_ACCESS_TOKEN: client_id, client_secret
S3_BUCKET_NAME: articles-metadata-bucket
GLUE_CRAWLER_NAME: articles-metadata-crawler

MY_AWS_CONN
AND 
# DEFAULT ID PW FOR AIRFLOW UI IS airflow: change if you need

