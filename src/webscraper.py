# import statements
import urllib2
import re
import mechanize
from bs4 import BeautifulSoup

# specify the url
quote_page = 'https://mtgdecks.net/Modern/tournaments/page:2'
# query the website and return the html to the variable page
page = urllib2.urlopen(quote_page)
# parse the html using beautiful soup and store in variable soup
soup = BeautifulSoup(page, 'html.parser')

str= r"[\x2D]"
counter = 0
for link in soup.find_all('a', attrs={'href':re.compile(str)}):
    if counter > 0 and counter <= 20:
        print(link.get('href'))
    counter += 1
