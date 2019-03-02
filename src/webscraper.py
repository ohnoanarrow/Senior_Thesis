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

tourn_num = 0

def PageParser(page_number):
""" This function iterates through the tournament pages and grabs tournament hrefs """
""" It also feeds the tournament number and tournament href into the DeckParser function"""

    # specify the url
    quote_page = 'https://mtgdecks.net/Modern/tournaments/page:' + page_number
    # query the website and return the html to the variable page
    page = requests.get(quote_page)
    # parse the html using beautiful soup and store in variable soup
    soup = BeautifulSoup(page.text, 'html.parser')

    str= r"[\x2D]"

    counter = 0
    for link in soup.find_all('a', attrs={'href':re.compile(str)}):
        if counter > 0 and counter <= 5: #TODO Change this back to 20
            decks_page = 'https://mtgdecks.net/' + link.get('href')
            print(decks_page)
            page = requests.get(decks_page)
            soupy = BeautifulSoup(page.text, 'html.parser')
            global tourn_num
            tourn_num += 1
            DeckParser(tourn_num, soupy)
        counter += 1

def DeckParser(tourn_num, soup):
""" This function iterates through the decks and finds their color"""
""" It also feeds the deck color, tournament number, deck rank, and deck href
    into the CardParser function"""

    # Isolating the top 4 decks
    none_counter = 0
    rank_counter = 1

    for tag in soup.find_all('tr'):
        placeholder_string = ""
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
                    color = x.get('class')
                    if color[0] != 'small-icon':
                        # Saves the color in a placeholder so I can manipulate the string contents
                        placeholder_string = color[2]
                        # Concatenating the single letter indicating color onto the color string
                        color_string += placeholder_string[3]
                # Sorting the letters in alphabetical order for dictionary reference
                color_string_sorter = sorted(color_string)
                color_string = ''.join(color_string_sorter)
                deck_color = color_dictionary.get(color_string)

                CardParser(tourn_num, rank_counter, deck_color, soupy)

                rank_counter += 1

def CardParser(tourn_num, rank, deck_color, soup):

def main():
    i = 1

    # TODO Change this back to go through all the pages
    # for i in range(1,3):
    PageParser(str(i))

if __name__ == '__main__':
    main()
