import os
import urllib.request
import xml.dom.minidom
import xml.etree.ElementTree as ET
from prettytable import PrettyTable
PT = PrettyTable()

def create_main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    # TODO: Logic for searching for URL Feeds
    print("1. Display Subscribed Feeds")

    # TODO: Write logic for displaying feeds for option 1.
        # * Need a function to build the menu for this option. This menu should display an option to input a URL, as well as a prompt
    print("2. Input New RSS URL")
    print("3. Exit\n")
    print("CHOOSE AN OPTION")
    pass

def main_menu_logic():
    create_main_menu()
    menu_selection = input(">> ")
    # TODO: Write some if statements to determine the function to be called based off of the menu choice.
    # TODO: Write the functions that handle the menu choices in a separate module.
    if menu_selection == "1":
        display_feeds_table()
        pass
    if menu_selection == "2":
        display_rss_url_search_menu()
    pass

def display_feeds_table(title, description, link):
    # TODO Need to try and format my own table. Draw it out first
    print('|' + '--' * 76 + '| \n')
    print('|' + '--' * 76 + '|')
    # PT.field_names = ['Title', 'Description', 'Link']
    # PT.add_row([title, description, link])
    # print(PT)
    pass

def display_rss_url_search_menu():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter an RSS URL: \n")
    RSS_URL_input = input('>> ') # Don't forget to change this back to regular input (>>) after testing
    get_rss_url(feed_to_search) # change this back to this: get_rss_url(RSS_URL_input)
    pass

feed_to_search = 'http://www.cbn.com/cbnnews/us/feed/'
# ? Test Feed URL: 'http://feeds.bbci.co.uk/news/world/rss.xml'
# ? Test Feed URL: 'http://www.cbn.com/cbnnews/us/feed/'
# ? Test Feed URL: 'https://thewest.com.au/rss-feeds'

"""
    XML documents have the following properties when returned:

    root will be the root tag, for which we can access attributes with that tag as a dictionary of attributes, much like html attributes like id, class etc.

"""

# Steps:
# 1. Get the root node of the XML Document
def get_rss_url(feed_url):
    # TODO: Save the XML response as a var in this function, then call ElementTree.parse() and pass the XML res as an arg
    # This request takes a URL as an argument and opens the url, then parses the response and returns an XML string.
    with urllib.request.urlopen(feed_url) as response:
        xml_response = response.read()
        # print(xml_response, '\n')

    dom = xml.dom.minidom.parseString(xml_response) # Parses the response to a string
    pretty_xml = dom.toprettyxml() # Prettify the response

    # user_passed_URL = feed_url
    # tree = ET.parse(pretty_xml)
    # print(tree)
    # TODO: typecheck the root tag to be <rss>
    root = ET.fromstring(pretty_xml) # grabs the root tag from the XML response [str], which will always be an RSS tag
    title_tag_list = root.findall('.//item') # Finds all tags named item in the XML response


    # TODO These values will need to be stored in a separate data structure.  The values will need to be pulled for displaying in the feeds table when the user inits the menu. Consider creating a function that fetches a few URLs once the program is ran, and loads those into the table.
    for item_tag in title_tag_list[1:11]: # limit the results to ten 
        article_title = item_tag[0].text[:10]
        # print('TITLE ==>', article_title[:50])
        article_description = item_tag[1].text[:10]
        # print('DESC ==>', article_description)
        article_link = item_tag[2].text
        # print('LINK ==>', article_link)
        pass
    display_feeds_table(article_title, article_description, article_link)
    pass
