"""this module contains handlers for any choice of extraction functionalities needed by the _engine.py"""

import re
from random import choice
from bs4 import BeautifulSoup

"""<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Extracters>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"""

def extract_agent() -> str:
    """return a random user agent name"""

    random_user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR'
    ]
    return choice(random_user_agent)
#print(extract_agent())

def extract_domain(https_url: str) -> str:
    """extract the main domain name from a given https url
        parameters:
            https_url: an https  url that will to be parser
        Return: domain name or None
    """

    # regex pattern to match the domain
    domain_pattern = r"https?://(www\.)?([a-zA-Z0-9.-]+)"
    success = re.search(domain_pattern, https_url)
    if success:
        # split domain/subdomain string into a list and remove any subdomain with length == 2 e.g EN, NG, FR, e.t.c
        domain = list(filter(lambda x: len(x) > 2, success.group(2).upper().split(".")))
        len_ = len(domain)
        if len_ > 0 and "WWW" != domain[0]:
            if len(domain) >= 3:
                return f"{domain[0]} {domain[-2]}"
            return domain[0]
        d = str(domain[1:len(domain) - 1]) if len_ > 0 else None
        return d  #str(domain[1:len(domain) - 1])
    return None


def extract_html(str_html: str) -> list:
    """strip and clean strings of html
         parameters:
              str_html: string of dirty html
         Return: clean strings of html
    """
    want = re.compile('<.*?>')
    html = re.sub(want, '', str_html)
    return html
#print(extract_domain("https://mu.ac.in/wp-content/uploads/2021/05/Data-Structure-Final-.pdf"))


"""<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<sorters>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"""

def sort_result(pages: list) -> list:
    """sort result pages based on sort value"""
    # page that has missing key values will put at the end of the list
    if pages and len(pages) >= 1:
        return sorted(pages, key=lambda x: x['sort'])


"""<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<cleaners>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"""

def clean_title(title=None):
    """remove https link in title"""
    pattern = r'https.*'
    if title:
        clean_title = re.sub(pattern, '', title)
        return clean_title


def clean_desc(desc=None):
    """ """
    pat1 = r'^Web'
    if desc:
        clean_desc = re.sub(pat1, '', desc)
        return clean_desc 


"""<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<parsers>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"""

def parse_google_results(html: str) -> list:
    """extract each answer page from google search result"""
    if html is None:
        return []

    soup = BeautifulSoup(html, "lxml")
    results = soup.find_all("div", class_="N54PNb BToiNc cvP2Ce")

    result_list = []
    incr, decr = 0, len(results) - 1
    for result in results:
        link = result.find('a').get("href")
        title = clean_title(result.a.text)
        domain = extract_domain(link)
        desc = clean_desc(result.find("div", class_="VwiC3b").text) if result.find("div", class_="VwiC3b") else "No description found"
        if desc != 'No description found':
            incr += 1
            sort_k = incr
        else:
            decr -= 1
            sort_k = desc
        result_list.append({"title": title, "domain": domain, "link": link, "description": desc, 'sort': sort_k})

    if len(result_list) > 1:
        return sort_result(result_list)

    return result_list


def parser_bing_results(html: str) -> list:
    """parse the html result doc from bing"""
    
    soup = BeautifulSoup(html, "lxml")
    results = soup.find_all("li", class_="b_algo")
    decr, incr = len(results), 0

    result_list = []
    for result in results:
        link = result.h2.a.get("href")
        title = clean_title(result.h2.a.string)
        domain = extract_domain(link)
        desc = clean_desc(result.find("p", class_="b_lineclamp2").text) if result.find("p", class_="b_lineclamp2") else "No description found"
        if desc != "No description found":
            incr += 1
            sort = incr
        else:
            decr -= 1
            sort = decr
        result_list.append({"title": title, "domain": domain, "link": link, "description": desc, 'sort': sort})

    if len(result_list) > 1:
        return sort_result(result_list)

    return result_list

