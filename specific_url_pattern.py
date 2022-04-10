from bs4 import BeautifulSoup
from requests import request
import requests
import re


class Website:
     def __init__(self, name, url, target_pattern, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.target_pattern = target_pattern
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag
class Content:

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

class Crawler:
    """
    The Crawler class is written to start from the home page of each site, locate internal links, and parse the content from each internal link found:
    """
    def __init__(self, site):
        self.site = site
        self.visited = []

    def get_page(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safe_get(self, page_obj, selector):
        selected_elem = page_obj.select(selector)
        if selected_elem is not None and len(selected_elem) > 0:
            return '\n'.join(elem.get_text for elem in selected_elem)
        return ''

    def parse(self, url):
        bs = self.get_page(url)
        if bs is not None:
            title = self.safe_get(bs, self.site.title_tag)
            body = self.safe_get(bs, self.site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print_()

    def crawl(self):
        """
        Get pages from website home page
        """
        bs = self.get_page(self.site.url)
        target_pages = bs.find_all('a', href = re.compile(self.site.target_pattern))
        for target_page in target_pages:
            target_page = target_page.attrs['href']
            if target_page not in self.visited:
                self.visited.append(target_page)
                if not self.site.absolute_url:
                    target_page = '{}{}'.format(self.site.url, target_page)
                self.parse(target_page)

reuters = Website('Reuters', 'https://www.reuters.com', '^(/article/)', False, 'h1', 'div.StandardArticleBody_body_1gnLA')
crawler = Crawler(reuters)
crawler.crawl()
