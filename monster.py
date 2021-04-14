import urllib.request
import xml.dom.minidom

with urllib.request.urlopen('http://news.yahoo.com/rss/') as response:
    xml_response = response.read()

dom = xml.dom.minidom.parseString(xml_response)
pretty_xml = dom.toprettyxml()
print(pretty_xml)