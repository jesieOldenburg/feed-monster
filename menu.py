import os
import urllib.request
import xml.dom.minidom
import xml.etree.ElementTree as ET
import shelve
from prettytable import PrettyTable

# TODO Use shelve to persist my data

PT = PrettyTable()

s = shelve.open('test.db')
try:
    s['test_dict'] = {'a': '1', 'b': '2', 'c': '3'}
    dbtest = s['test_dict']
finally:
    s.close()

print(dbtest)

def create_main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    # TODO: Write logic for displaying feeds for option 1.
    print("1. Display Subscribed Feeds")
    print("2. Input New RSS URL")
    print("3. Exit\n")
    print("4. Refresh Feeds")
    print("CHOOSE AN OPTION")
    pass

def main_menu_logic():
    create_main_menu()
    menu_selection = input(">> ")
    # TODO: Write the functions that handle the menu choices in a separate module.
    if menu_selection == "1":
        display_feeds_table()
        pass
    if menu_selection == "2":
        display_rss_url_search_menu()
    pass

def display_feeds_table():
    # TODO Need to try and format my own table. Draw it out first
    PT.field_names = ['Title', 'Description', 'Link']
    # print(PT)
    pass

def create_table_rows(title, desc, link):
    PT.add_row([title, desc, link])
    

def display_rss_url_search_menu():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter an RSS URL: \n")
    RSS_URL_input = input('>> ') # Don't forget to change this back to regular input (>>) after testing
    get_rss_url(feed_to_search) # change this back to this: get_rss_url(RSS_URL_input)
    pass

feed_to_search = 'http://feeds.bbci.co.uk/news/world/rss.xml'
# ? Test Feed URL: 'http://feeds.bbci.co.uk/news/world/rss.xml'
# ? Test Feed URL: 'http://www.cbn.com/cbnnews/us/feed/'
# ? Test Feed URL: 'https://thewest.com.au/rss-feeds'

"""
    XML documents have the following properties when returned:

    root will be the root tag, for which we can access attributes with that tag as a dictionary of attributes, much like html attributes like id, class etc.

"""

def store_data(d):
    # Needs to use shelve to persist the data
    SH = shelve.open('feeds.db')
    try:
        SH['feeds'] = d
        SUBBED_FEEDS = SH['feeds']
    finally:
        SH.close()
    print('SUB FEED', SUBBED_FEEDS)

master_dict = {
    'feeds': {}
}

def parse_XML(xml_str):
    # TODO: typecheck the root tag to be <rss>
    root = ET.fromstring(xml_str) # grabs the root tag from the XML response [str], which will always be an RSS tag
    title_tag_list = root.findall('.//item') # Finds all tags named item in the XML response
    feed_title = root[0][0].text
    feed_link = root[0][1].text
    print('feed title', root[0][1].text)
    display_feeds_table()
    
    if feed_title in master_dict['feeds'].keys():
        print('You are already subscribed to this feed')
    else: 
        master_dict['feeds'][feed_title] = feed_link
        store_data(master_dict)
        pass
    print(master_dict)
    # TODO These values will need to be stored in a separate data structure.  The values will need to be pulled for displaying in the feeds table when the user inits the menu. Consider creating a function that fetches a few URLs once the program is ran, and loads those into the table.
    for item_tag in title_tag_list[1:11]: # limit the results to ten 
        article_title = item_tag[0].text[:10]
        # print('TITLE ==>', article_title[:50])
        article_description = item_tag[1].text[:10]
        # print('DESC ==>', article_description)
        article_link = item_tag[3].tag # Change me back to link # TODO: Figure out how to put the url into a different string
        # print('LINK ==>', ite)
        create_table_rows(article_title, article_description, article_link) # ! This will need to move. TEST ONLY!
        pass
    print(PT)
    # display_feeds_table(article_title, article_description, article_link)
    # TODO: Display a prompt asking if the user would like to enter another url, or return to the main menu. Offer this choice as a Y/n option
    # ! Remove this after using as a test case. 
    pass

# Steps:
# 1. Get the root node of the XML Document
def get_rss_url(feed_url):
    # TODO: Save the XML response as a var in this function, then call ElementTree.parse() and pass the XML res as an arg
    # This request takes a URL as an argument and opens the url, then parses the response and returns an XML string.
    try:
        with urllib.request.urlopen(feed_url) as response:
            xml_response = response.read()
    except:
        print('An exception occurred')
        # print(xml_response, '\n')

    dom = xml.dom.minidom.parseString(xml_response) # Parses the response to a string
    xml_response = dom.toprettyxml() # Prettify the response
    parse_XML(xml_response)
    # user_passed_URL = feed_url
    # tree = ET.parse(pretty_xml)
    # print(tree)
    
