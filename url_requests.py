def get_rss_url(feed_url, whocall):
    """This function accepts an RSS feed URL and fetches an XML response. It then formats the response into a string and passes it to a parser function

    Args:
        feed_url (string): A url represented as a string
        whocall (string): A keyword argument used in a logical statement
    """    
    try:
        with urllib.request.urlopen(feed_url) as response:
            xml_response = response.read()
    except:
        print('An exception occurred')
        # print(xml_response, '\n')

    dom = xml.dom.minidom.parseString(xml_response) # Parses the response to a string
    xml_response = dom.toprettyxml() # Prettify the response
    # print(xml_response)
    if whocall == "url_search":
        print("search called me ")
        parse_XML(xml_response, feed_url, whocall="url_search")
        pass
    if whocall == "pull_subs":
        PT.clear_rows()
        parse_XML(xml_response, feed_url, whocall="pull_subs")
    #     pass
    # user_passed_URL = feed_url
    # tree = ET.parse(pretty_xml)
