import os
import json
import pathlib
import datetime as dt
import pandas as pd

from airflow import DAG
import airflow.utils.dates
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from custom.operators import GlueTriggerCrawlerOperator



with DAG(
    dag_id="collect_featured_articles_metadata",
    description="Download metadata of daily feature articles from Wikipedia, transform, upload to S3 and Run Glue Crawler",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@daily",
) as dag:

    
    get_access_token = BashOperator(
        task_id = "get_access_token",
        bash_command=(
            'curl -X POST -d "grant_type=client_credentials" '
            '-d "client_id={{ var.json.WIKI_ACCESS_TOKEN.client_id }}" '
            '-d "client_secret={{ var.json.WIKI_ACCESS_TOKEN.client_secret }}" '
            'https://meta.wikimedia.org/w/rest.php/oauth2/access_token'
        ),
        do_xcom_push=True,
    )


    download_articles = BashOperator(
        task_id="download_articles",
        bash_command=(
            'token="{{ task_instance.xcom_pull(task_ids=\'get_access_token\', key=\'return_value\') }}" &&'
            "export ACCESS_TOKEN=$(echo $token | awk -v FS=: '{print $4}' | sed 's/}//') &&"
            'curl -H "Authorization: Bearer $ACCESS_TOKEN" '
            'https://api.wikimedia.org/feed/v1/wikipedia/en/featured/'
            '{{ execution_date.strftime("%Y/%m/%d") }} '
            '| json_pp > /opt/airflow/data/articles_metadata.json'
        ),
    )

    
    def _upload_metadata(timestamp, input_path, output_path, s3_conn_id, s3_bucket):

        # Open json as dataframe 
        data = json.load(open(input_path))
        df = pd.DataFrame(data['onthisday'])

        # Extract and create columns/dataframe
        df['timestamp'] = timestamp
        df['wikibase_item'] = (df['pages'].astype(str))\
                                .str.split("wikibase_item': '").str[1]\
                                .str.split("'}").str[0]
        df['title'] = (df['pages'].astype(str))\
                        .str.split("normalizedtitle': '").str[1]\
                        .str.split("',").str[0]
        df['description'] = (df['pages'].astype(str))\
                                .str.split("description': '").str[1]\
                                .str.split("',").str[0]
        df['extract'] = (df['pages'].astype(str))\
                            .str.split("extract': '").str[1]\
                            .str.split("',").str[0]
    
        df = df[[ "timestamp", "wikibase_item", "title", "description", "extract" ]]
        df.to_csv(output_path, sep='\t', index=False, header=True) 

        # Upload file to S3
        s3_hook = S3Hook(s3_conn_id)
        s3_hook.load_file(
                output_path,
                key=f"Wikipedia/{timestamp}.tsv",
                bucket_name=s3_bucket,
                replace=True,
            )

    upload_metadata = PythonOperator(
        task_id="upload_metadata",
        python_callable=_upload_metadata,
        op_kwargs={
            'timestamp': '{{ execution_date.strftime("%Y-%m-%d") }}',
            'input_path': '/opt/airflow/data/articles_metadata.json', 
            'output_path': '/opt/airflow/data/articles_metadata.tsv',
            's3_conn_id': 'MY_AWS_CONN',
            's3_bucket': '{{ var.value.S3_BUCKET_NAME }}'   
        },
    )

    
    trigger_crawler = GlueTriggerCrawlerOperator(
        aws_conn_id='MY_AWS_CONN',
        task_id='trigger_crawler',
        crawler_name='{{ var.value.GLUE_CRAWLER_NAME }}'   
    )


    get_access_token >> download_articles >> upload_metadata >> trigger_crawler



