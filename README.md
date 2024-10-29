# ETL Pipeline for Creating a Catalog of Featured Articles on AWS
This Airflow pipeline has been developed to collect metadata of featured articles from Wikipedia, for creating a data lake on AWS. It 1) fetches metadata of daily featured articles from Wikimedia, 2) filters and cleans the dataset and 3) uploads the dataset to S3 and triggers AWS Glue crawler. It creates/updates the Glue data catalog on a daily basis, and you can easily query the catalog using AWS Athena. The future goal of this project is to build a basis of a collective article collection on AWS, by adding more data sources.


## Prerequisite
1.  **Wikimedia Cliend Id and Client Secret**\
  Take a look at [Getting started with Wikimedia APIs](https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs)
2.  **AWS Stack**\
  Create an S3 bucket and Glue Crawler using AWS the Cloud Formation Template (`aws_create_stack.yaml`). Make sure that the name of the S3 bucket is *articles-metadata-bucket*, and you download AWS access key.
3.  **Docker Desktop**\
  Installation guide on the official website is [here](https://docs.docker.com/compose/install/)
   

## How to Run
1. Git clone and Set up directory structure
```
git clone https://github.com/SLI239/featured_articles_metadata_etl.git
cd featured_articles_metadata_etl
mkdir ./config ./data ./logs ./plugins
```
2. Build Docker image and run Docker Compose
```
docker build --build-arg AIRFLOW_VERSION=2.10.2 -t apache/airflow-custom:2.10.2 .
docker-compose up
```
3. Set up variables and connections on Airflow web UI
Default ID and Password for login is `airflow`

- Variables
  
| Key                     | Value   | 
| ----------------------- | ------- | 
|  **WIKI_ACCESS_TOKEN**  | *{"client_id":"`your client id`", "client_secret":"`your client secret`"}* | 
|  **S3_BUCKET_NAME**     | *articles-metadata-bucket*  | 
|  **GLUE_CRAWLER_NAME**  | *articles-metadata-crawler* | 

- Connections

| Conn Id            | Conn Type    | Extra        | 
| ----------------------- | ------- | ----------------------- | 
| **MY_AWS_CONN**    | AWS Web Services | {"aws_access_key_id":"`your access key Id`", "aws_secret_access_key": "`your secret access key`"} |


## Note
- **Take extra caution in securing Wikimedia token**: The API token type is bearer token and it is pushed to XCom, and can be easily found on the Web UI
- `GlueTriggerCrawlerOperator` is from [data-pipelines-with-apache-airflow](https://github.com/BasPH/data-pipelines-with-apache-airflow/blob/master/chapter16/dags/custom/operators.py)
- More information about running Airflow with the CeleryExecutor in Docker is [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)


