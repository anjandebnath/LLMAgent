# agent_aj/pipelines/crawling_pipeline.py
# This script defines the ZenML pipeline that connects the steps.

from zenml import pipeline
from typing import List
from ..steps.crawl_step import crawl_social_media_posts
from ..steps.store_step import store_data_in_mongodb

# Concept: ZenML Pipeline
# The '@pipeline' decorator defines the workflow of our ETL process.
# It chains together the steps ('crawl_social_media_posts' and
# 'store_data_in_mongodb') by managing their inputs and outputs.
# ZenML handles the execution order and data passing between steps.
@pipeline
def social_media_etl_pipeline(
    linkedin_urls: List[str],
    medium_urls: List[str]
):
    """
    Defines the ETL pipeline for crawling and storing social media data.
    """
    print(">>> Pipeline execution started.")
    
    # The output of the first step is automatically passed as input
    # to the second step where the parameter name matches the output name.
    crawled_data = crawl_social_media_posts(
        linkedin_urls=linkedin_urls,
        medium_urls=medium_urls
    )
    
    store_data_in_mongodb(data=crawled_data)
    
    print(">>> Pipeline execution finished.")
