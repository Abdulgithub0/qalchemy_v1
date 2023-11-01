"""google v1 implementation"""

import requests
from search_aggregate.extractor import extract_agent, parse_google_results
import time


def make_google_request(user_query: str, max_retries=4) -> str:
    """perform google search using exponential backoff strategy"""
    base_url = "https://www.google.com/search"
    params = {"q": user_query}
    
    for retry in range(1, max_retries):
        try:
            response = requests.get(base_url, headers={'User-Agent': extract_agent()}, params=params, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            if retry < max_retries:
                # Calculate the backoff delay using exponential backoff strategy
                backoff_delay = 2 ** retry

                # would log this into log file later before deployment.
                print(f"Retrying GOOGLE in {backoff_delay} seconds...")
                
                # kindly rest to avoid google trouble
                time.sleep(backoff_delay)
            else:
                print(f"Max retries exceeded. GOOGLE Request failed.")
                return None


def google(user_query):
    """interface to this google module"""
    html = make_google_request(user_query)
    results = parse_google_results(html)
    return results

#print(google("data structure and algorithms"))
