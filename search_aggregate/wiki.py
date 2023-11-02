import requests
from search_aggregate.extractor import extract_html, extract_agent
import time

#"https://en.wikipedia.org/wiki/Special:Search"

def wiki(user_query: str, max_retries=4) -> list:
    """query wikipedia rest service using user_query query input
        
       parameters:
            user_query: string of characters that will be query out of database
       Return: list obj
    """

    url = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + user_query

    for retry in range(1, max_retries):
        try:
            response = requests.get(url, headers={'User-Agent': extract_agent()}, timeout=5)
            response.raise_for_status()

            results = response.json()
            info = {}
            info['description'] = extract_html(results.get('description'))
            info['title'] = extract_html(results.get('displaytitle'))
            info['extract'] = extract_html(results.get('extract'))
            info['thumbnail_url'] = extract_html(results['thumbnail'].get('source')) if results.get('thumbnail') else None
            info['page_url'] = extract_html(results['content_urls']['desktop'].get('page')) if results.get('content_urls') and results['content_urls'].get('desktop') else None
            return [info]
        except requests.exceptions.RequestException as e:
            if retry < max_retries - 1:
                delay = 2 ** retry 
                print(f"Retrying Wiki in {delay} seconds...")
                time.sleep(delay)
    print(f"Max retries exceeded. Wiki Request failed.")
    return None 

#print(wiki("exponential backoff"))
