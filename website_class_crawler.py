"""
Crawler to scrape the title and content of any URL that is provided for a given web page from a given website:
"""
import requests
from bs4 import BeautifulSoup

class Content:
    """
    Common base class for all articles/pages
    """

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print_(self):
        """
        Flexible printing function controls output
        """
        print("URL: {}".format(self.url))
        print("Title: {}".format(self.title))
        print("Body:\n{}".format(self.body))

class Website:
    """
    Contains informations about website structure
    """

    def __init__(self, name, url, title_tag, body_tag):
        self.name = name
        self.url = url
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
        selected_elem = page_obj.select(selector)
        if selected_elem is not None and len(selected_elem) > 0:
            return '\n'.join([elem.get_text() for elem in selected_elem])
        return ''

    def parse(self, site, url):
        """
        Extract content from a given page url
        """
        bs = self.get_webpage(url)
        if bs is not None:
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print_()
            else:
                print("There is no empty string and somthing is wrong with the url")

crawler = Crawler()

site_data = [['O\'Reilly Media', 'http://oreilly.com', 'h1', 'section#product-description'], ['Reuters', 'http://reuters.com', 'h1', 'div.StandardArticleBody_body_1gnLA'], ['Brookings', 'http://www.brookings.edu', 'h1', 'div.post-body'], ['New York Times', 'http://nytimes.com', 'h1', 'p.story-content']]

websites = []
for row in site_data:
    websites.append(Website(row[0], row[1], row[2], row[3]))

crawler.parse(websites[0], 'http://shop.oreilly.com/product/' '0636920028154.do')
crawler.parse(websites[1], 'http://www.reuters.com/article/' 'us-usa-epa-pruitt-idUSKBN19W2D0')
crawler.parse(websites[2], 'https://www.brookings.edu/blog/' 'techtank/2016/03/01 idea-to-retire-old-methods-of-policy-education/')
crawler.parse(websites[3], 'https://www.nytimes.com/2018/01/' '28/business/energy-environment/oil-boom.html')