# run_pipeline.py
# This is the entry point script to execute our ZenML pipeline.

from agent_aj.pipelines.crawling_pipeline import social_media_etl_pipeline
from typing import List

def run_etl():
    """
    Configures and runs the social media ETL pipeline.
    """
    # --- Configuration ---
    # TODO: Replace these with your actual post URLs
    # For this example, we are using placeholder URLs.
    # The crawlers are designed to handle potential failures gracefully.
    linkedin_post_urls: List[str] = [
        "https://www.linkedin.com/posts/anjan-debnath-77183033_github-anjandebnathspringaibot-with-spring-activity-7344747397467525120-Fb0z?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAcQR0UBZOlKAvwkiiw8RKpS5NT3kracTn8",
        "https://www.linkedin.com/posts/anjan-debnath-77183033_cloud-cost-plan-activity-7324319491134251008-elxk?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAcQR0UBZOlKAvwkiiw8RKpS5NT3kracTn8",
        "https://www.linkedin.com/posts/anjan-debnath-77183033_github-anjandebnathk8-terraform-under-activity-7309221513889554432-mVGg?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAcQR0UBZOlKAvwkiiw8RKpS5NT3kracTn8",
        "https://www.linkedin.com/posts/anjan-debnath-77183033_deeplearning-pytorch-lora-activity-7294610511260721152-ED86?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAcQR0UBZOlKAvwkiiw8RKpS5NT3kracTn8",
        "https://www.linkedin.com/posts/anjan-debnath-77183033_cloud-architect-system-activity-7286391591521435648-YBtO?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAcQR0UBZOlKAvwkiiw8RKpS5NT3kracTn8"
    ]

    medium_post_urls: List[str] = [
        "https://anjancse07.medium.com/solution-of-the-exercises-chapter-1-the-machine-learning-landscape-bc3cccef8d12",
        "https://anjancse07.medium.com/how-to-take-ielts-preparation-as-a-professional-in-the-it-business-freelancing-any-job-sector-3be6e6f59026",
        "https://anjancse07.medium.com/how-to-take-ielts-preparation-as-a-professional-in-the-it-business-freelancing-any-job-sector-fd913ac4ebbf",
        "https://anjancse07.medium.com/solution-of-the-exercise-chapter-7-ensemble-learning-and-random-forest-27102a0a18db",
        "https://anjancse07.medium.com/solution-of-chapter-6-decision-tree-e6bb6f729a5b"
    ]
    # --- End Configuration ---

    print("Initializing and running the ETL pipeline...")
    
    # Here, we instantiate the pipeline with our configuration
    # and then run it.
    pipeline_instance = social_media_etl_pipeline(
        linkedin_urls=linkedin_post_urls,
        medium_urls=medium_post_urls
    )

    # pipeline_instance.run()

    print("\nPipeline run initiated. Check your terminal for logs from the steps.")
    print("After completion, you can connect to your MongoDB instance to verify the data.")


if __name__ == "__main__":
    # This standard Python construct ensures that the 'run_etl' function
    # is called only when the script is executed directly.
    run_etl()
