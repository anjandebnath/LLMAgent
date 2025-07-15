# agent_aj/steps/crawl_step.py
# This script defines a ZenML step for our pipeline.

from zenml import step
from typing import List, Dict, Any, Annotated
from ..data_crawler import LinkedInCrawler, MediumCrawler

# Concept: Decorators
# The '@step' decorator from ZenML transforms this Python function into a
# ZenML step. This allows it to be used within a ZenML pipeline,
# enabling features like caching, tracking, and orchestration.
@step
def crawl_social_media_posts(
    linkedin_urls: List[str],
    medium_urls: List[str]
) -> Annotated[List[Dict[str, Any]], "crawled_data"]:
    """
    A ZenML step that crawls data from LinkedIn and Medium.

    Args:
        linkedin_urls: A list of URLs to LinkedIn posts.
        medium_urls: A list of URLs to Medium articles.

    Returns:
        A list of dictionaries containing the crawled data.
    """
    print("--- Starting Crawl Step ---")
    # Concept: Polymorphism
    # We can treat both LinkedInCrawler and MediumCrawler objects as instances
    # of the base DataCrawler class. Here, we are using their specific
    # implementations to crawl data from different sources.
    linkedin_crawler = LinkedInCrawler()
    medium_crawler = MediumCrawler()

    linkedin_data = linkedin_crawler.crawl(linkedin_urls)
    medium_data = medium_crawler.crawl(medium_urls)

    all_data = linkedin_data + medium_data
    print(f"--- Crawl Step Finished: Found {len(all_data)} total posts. ---")
    return all_data
