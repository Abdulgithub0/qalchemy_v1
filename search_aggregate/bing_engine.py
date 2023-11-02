""" bing search implementation - v1"""

import requests
import lxml
from search_aggregate.extractor import extract_agent, parser_bing_results
import time


def make_bing_request(user_query: str, max_retries=4) -> list:
    """perform bing search using exponential backoff"""

    url = "https://www.bing.com/search"
    query = {"q": user_query}

    for retry_time in range(1, max_retries):
        try:
            response = requests.get(url, headers={'User-Agent': extract_agent()}, params=query, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as err:
            if retry_time < max_retries - 1:
                # find backoff delay time
                delay_time = 2 ** retry_time
                print(f"Retrying BING in {delay_time} seconds...")
                time.sleep(delay_time)
    print(f"max retries exceeded. BING Request failed")
    return None


def bing(user_query: str) -> list:
    """main interface to this module"""
    return parser_bing_results(make_bing_request(user_query))

#print(bing("data structure and algorithms"))

