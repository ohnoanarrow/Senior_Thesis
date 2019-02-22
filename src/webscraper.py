# import statements
# from urllib.request import urlopen
# import mechanize
import requests
import re
from itertools import cycle
from bs4 import BeautifulSoup

color_dictionary = {
    "u": "mono blue",
    "w": "mono white",
    "g": "mono green",
    "r": "mono red",
    "b": "mono black",
    "uw": "azorius",
    "bu": "dimir",
    "br": "rakdos",
    "gr": "gruul",
    "gw": "selesnya",
    "bw": "orzhov",
    "ru": "izzet",
    "bg": "golgari",
    "rw": "boros",
    "gu": "simic",
    "bgr": "jund",
    "guw": "bant",
    "bru": "grixis",
    "grw": "naya",
    "buw": "esper",
    "ruw": "jeskai",
    "brw": "mardu",
    "bgu": "sultai",
    "gru": "temur",
    "bgw": "abzan",
    "bgru": "chaos",
    "bgrw": "aggression",
    "bguw": "growth",
    "bruw": "artifice",
    "gruw": "altruism",
    "bgruw": "rainbow"
}


# specify the url
quote_page = 'https://mtgdecks.net/Modern/modern-libourne-is-magic-4-libourne-tournament-54073'
# query the website and return the html to the variable page
page = requests.get(quote_page)
# parse the html using beautiful soup and store in variable soup
soup = BeautifulSoup(page.text, 'html.parser')

# Keep these on the VERY OUTSIDE OF ALL LOOPS, THESE ARE NOT TO BE RESET
sb_id = 0
tourn_num = 0
str= r"[\x2D]"

# Isolating the top 4 decks
none_counter = 0
rank_counter = 1

for tag in soup.find_all('tr'):
    color_string = ""
    sb_color_string = ""
    # The strong tag will first come up with deck ranking
    if tag.strong is None:
        none_counter += 1
    # This is where we pull the top 4 decks
    if none_counter > 0 and none_counter < 2 and rank_counter <= 4:
        # Making sure there is a value under the strong tag
        if tag.strong is not None:
            color = tag.find('div', attrs={'class':"small"})
            for x in color.contents:
                print(x)
            rank_counter += 1
