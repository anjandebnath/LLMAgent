# agent_aj/data_crawler.py
# This script demonstrates Abstraction and Inheritance, core OOP concepts.

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

# Concept: Abstraction
# We define an abstract base class (ABC) 'DataCrawler'.
# It defines a contract for what subclasses must implement (the 'crawl' method)
# without specifying how they should do it. This allows for different types
# of crawlers (LinkedIn, Medium) that share a common interface.
class DataCrawler(ABC):
    """Abstract base class for a data crawler."""

    @abstractmethod
    def crawl(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Abstract method to crawl data from a list of URLs.
        Subclasses must implement this method.
        """
        pass

# Concept: Inheritance
# LinkedInCrawler inherits from DataCrawler. It provides a concrete
# implementation of the 'crawl' method specific to LinkedIn.
class LinkedInCrawler(DataCrawler):
    """A crawler for LinkedIn posts."""

    def crawl(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Crawls LinkedIn post URLs and extracts content.

        NOTE: This is a placeholder implementation. Real-world scraping of
        LinkedIn is complex, often requires authentication, and may be
        against their terms of service. This is for educational purposes.
        """
        crawled_data = []
        for url in urls:
            try:
                print(f"Crawling LinkedIn URL: {url}")
                # A real implementation would involve handling logins,
                # using browser automation tools like Selenium, and
                # parsing dynamic JavaScript-rendered content.
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                response.raise_for_status() # Raises an HTTPError for bad responses

                soup = BeautifulSoup(response.content, 'html.parser')
                
                # This is a hypothetical structure of a LinkedIn post page.
                # You would need to inspect the actual page source to find the correct selectors.
                post_content_element = soup.find("div", class_="share-update-section__update-content")
                content = post_content_element.text.strip() if post_content_element else "Content not found"

                crawled_data.append({
                    "source": "linkedin",
                    "url": url,
                    "content": content,
                })
            except requests.exceptions.RequestException as e:
                print(f"Error crawling {url}: {e}")

        return crawled_data

# Concept: Inheritance
# MediumCrawler also inherits from DataCrawler, providing its own
# implementation of 'crawl' for Medium articles.
class MediumCrawler(DataCrawler):
    """A crawler for Medium posts."""

    def crawl(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Crawls Medium post URLs and extracts content."""
        crawled_data = []
        for url in urls:
            try:
                print(f"Crawling Medium URL: {url}")
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Medium articles are often within <article> tags.
                # This is a simplified selector.
                article_body = soup.find('article')
                if article_body:
                    paragraphs = article_body.find_all('p')
                    content = "\n".join([p.text for p in paragraphs])
                else:
                    content = "Content not found"

                crawled_data.append({
                    "source": "medium",
                    "url": url,
                    "content": content
                })
            except requests.exceptions.RequestException as e:
                print(f"Error crawling {url}: {e}")

        return crawled_data
