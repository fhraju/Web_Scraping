"""
Crawler to scrape the title and content of any URL from search :
"""
from pydoc_data.topics import topics
from turtle import title
import requests
from bs4 import BeautifulSoup

class Content:
    """
    Common base class for all articles/pages
    """

    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print_(self):
        """
        Flexible printing function controls output
        """
        print("New article found for topic: {}".format(self.topic))
        print("URL: {}".format(self.url))
        print("Title: {}".format(self.title))
        print("Body:\n{}".format(self.body))

class Website:
    """
    Contains informations about website structure
    """

    def __init__(self, name, url, search_url, result_listing, result_url, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.search_url = search_url
        self.result_listing = result_listing
        self.result_url = result_url
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag

class Crawler:

    def get_webpage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')
    
    def safe_get(self, page_obj, selector):
        """
        Utitlity function used to get a content string from a Beautiful Soup object and a selector.
        Return an empty string if no object is found for the given selector
        """
        child_obj = page_obj.select(selector)
        if child_obj is not None and len(child_obj) > 0:
            return child_obj[0].get_text()
        return ""

    def search(self, topic, site):
        """
        Searches a given website for a given topic and records all pages found
        """
        bs = self.get_webpage(site.search_url + topic)
        search_result = bs.select(site.result_listing)
        for result in search_result:
            url = result.select(site.result_url)[0].attrs['href']
            # Check to see whether it is a relative or an absolute url
            if (site.absolute_url):
                bs = self.get_webpage(url)
            else:
                bs = self.get_webpage(site.url + url)
            if bs is None:
                print("Something was wrong with that page or url. Skipping!")
                return
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(topic, title, body, url)
                content.print_()


    # def parse(self, site, url):
    #     """
    #     Extract content from a given page url
    #     """
    #     bs = self.get_webpage(url)
    #     if bs is not None:
    #         title = self.safe_get(bs, site.title_tag)
    #         body = self.safe_get(bs, site.body_tag)
    #         if title != '' and body != '':
    #             content = Content(url, title, body)
    #             content.print_()
    #         else:
    #             print("There is no empty string and somthing is wrong with the url")

crawler = Crawler()

site_data = [['O\'Reilly Media', 'http://oreilly.com', 'https://ssearch.oreilly.com/?q=','article.product-result', 'p.title a', True, 'h1', 'section#product-description'], ['Reuters', 'http://reuters.com', 'http://www.reuters.com/search/news?blob=', 'div.search-result-content','h3.search-result-title a', False, 'h1', 'div.StandardArticleBody_body_1gnLA'], ['Brookings', 'http://www.brookings.edu', 'https://www.brookings.edu/search/?s=', 'div.list-content article', 'h4.title a', True, 'h1','div.post-body']]

websites = []
for row in site_data:
    websites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

topics =['python', 'data science']
for topic in topics:
    print("Getting info about: " + topic)
    for target_site in websites:
        crawler.search(topic, target_site)
