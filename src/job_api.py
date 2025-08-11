from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))


def fetch_linkedin_jobs(search_query, location="france", rows=60):
    run_input = {
    "title": search_query,
    "location": location,
    "rows": rows,
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


def fetch_naukri_jobs(search_query, location="france", rows=60):
    run_input = {
    "keyword":search_query,
    "maxJobs":60,
    "freshness":"all",
    "sortBy":"relevance",
    "experience":"all",
        }
    
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    # Run the Actor and wait for it to finish
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs
