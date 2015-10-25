import requests
from bs4 import BeautifulSoup
import sys

def fetch_search_results(query=None, minAsk=None, maxAsk=None, bedrooms=None):
    search_params = {
        key: val for key, val in locals().items() if val is not None #locals() returns dictionary of current namespaces
    }
    if not search_params:
        raise ValueError("No valid keywords")

    base = 'https://newyork.craigslist.org/search/aap'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()  # <- no-op if status==200
    return resp.content, resp.encoding

def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed

def extract_listings(parsed): 
    """Returning a list of individual listings
    """
    listings = parsed.find_all('p', class_='row') #find_all is a beautifulsoup method
    extracted = []
    for listing in listings:
        link = listing.find('span', class_='pl').find('a')
        this_listing = {
            'description': link.string.strip()
        }
        extracted.append(this_listing)
    return extracted


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test': #sys.argv[1] is first argument after the script
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(
            minAsk=1500, maxAsk=6000, bedrooms=2
        )
    doc = parse_source(html, encoding)
    listings = extract_listings(doc)
    print len(listings)
    #print doc.prettify(encoding=encoding)









