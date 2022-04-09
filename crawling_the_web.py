from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import random
import datetime

pages = set()
random.seed(datetime.datetime.now)

# Retrieves a list of all internal links found on a page
def getInternalLInks(bs, include_url):
    include_url = '{}://{}'.format(urlparse(include_url).scheme,urlparse(include_url).netloc)
    internal_link= []
    # find all links that begin with a "/"
    for link in bs.find_all('a', href=re.compile('^(/|.*'+include_url+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_link:
                if (link.attrs['href'].startswith('/')):
                    internal_link.append(include_url + link.attrs['href'])
                else:
                    internal_link.append(link.attrs['href'])
    return internal_link

# Retrieves a list of External Links found on a page
def getExternalLinks(bs, exclude_url):
    external_links = []
    # Finds all links that start with "http" that do not contain the current URL
    for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+exclude_url+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links

def getRandomExternalLinks(starting_page):
    html = urlopen(starting_page)
    bs = BeautifulSoup(html, 'html.parser')
    external_links = getExternalLinks(bs, urlparse(starting_page).netloc)
    if len(external_links) == 0:
        print('No External links, looking around the site for one')
        domain = '{}://{}'.format(urlparse(starting_page).scheme,urlparse(starting_page).netloc)
        internal_links = getInternalLInks(bs, domain)
        return getRandomExternalLinks(internal_links[random.randint(0, len(internal_links)-1)])
    else:
        return external_links[random.randint(0, len(external_links)-1)]

def followExternalOnly(starting_site):