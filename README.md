# featured_article_metadata_etl
Airflow ETL pipeline for creating data lake for featured articles on AWS


- ADD MISSING FILE: IN dag

# 0. CREATE AWS STACK USING AWS CFT: SUBMIT create_stack.yaml
MAKE SURE THE NAME OF THE S3 IS: articles-metadata-bucket
ALSO GET CREDENTIALS (CLIENT ID AND SECRET) FOR WIKIMEDIA API

# 1. BUILD DOCKER IMAGE WITH PYTHON PACKAGES NEEDED
docker build --build-arg AIRFLOW_VERSION=2.10.2 -t apache/airflow-custom:2.10.2 .

# 2. CREATE .env AND RUN DOCKER COMPOSE
docker-compose up

# 3. SET UP CONNECTIONS AND VARIABLES ON THE WEB UI
WIKI_ACCESS_TOKEN: client_id, client_secret
S3_BUCKET_NAME: articles-metadata-bucket
GLUE_CRAWLER_NAME: articles-metadata-crawler

MY_AWS_CONN

# DEFAULT ID PW FOR AIRFLOW UI IS airflow: change if you need

