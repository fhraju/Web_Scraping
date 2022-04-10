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
    external_link = getRandomExternalLinks(starting_site)
    print("Random External link is: {}".format(external_link))
    followExternalOnly(external_link)

#followExternalOnly('http://oreilly.com')

# Collects a list of all external urls found on the site
all_ext_links = set()
all_int_links = set()

def getAllExternalLinks(site_url):
    html = urlopen(site_url)
    domain = '{}://{}'.format(urlparse(site_url).scheme,urlparse(site_url).netloc)
    bs = BeautifulSoup(html, 'html.parser')
    internal_link = getInternalLInks(bs, domain)
    external_link = getExternalLinks(bs, domain)

    for link in external_link:
        if link not in all_ext_links:
            all_ext_links.add(link)
            print(link)
    for link in internal_link:
        if link not in all_int_links:
            all_int_links.add(link)
            getAllExternalLinks(link)
all_int_links.add('http://oreilly.com')
getAllExternalLinks('http://oreilly.com')