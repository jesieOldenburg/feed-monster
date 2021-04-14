import os
import urllib.request
import xml.dom.minidom
import xml.etree.ElementTree as ET

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
        pass
    if menu_selection == "2": 
        display_rss_url_search_menu()
    pass

def display_feeds_table():
    pass

def display_rss_url_search_menu():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter an RSS URL: \n")
    RSS_URL_input = input('>> ') # Don't forget to change this back to regular input (>>) after testing
    get_rss_url(feed_to_search) # change this back to this: get_rss_url(RSS_URL_input)
    pass

feed_to_search = 'http://news.yahoo.com/rss/'

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
    
    dom = xml.dom.minidom.parseString(xml_response) # Parses the response to a string
    pretty_xml = dom.toprettyxml()
    # print(pretty_xml)
    
    # user_passed_URL = feed_url
    # tree = ET.parse(pretty_xml)
    # print(tree)
    root = ET.fromstring(pretty_xml)
    # print(root.attrib)
    for child in root:
        article_title = root[0][8][0].text
        article_link = root[0][8][1].text
        print(root[0][8][0].text)
        pass
    
    pass