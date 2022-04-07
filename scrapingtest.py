from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('https://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

images = bs.find_all('img',{'src':re.compile('\.\.\/img\gifts/img.*\.jpg')})
for img in images:
    print(img['src'])

# namelist = bs.find_all('span', {'class':'green'})
# for name in namelist:
#     print(name.get_text())
# namelist = bs.find_all(text='the prince')
# print(len(namelist))
# title = bs.find_all(id='title', class_='text')
# print(title)
# for child in bs.find('table',{'id':'giftlist'}).children:
#     print(child)

# #[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)