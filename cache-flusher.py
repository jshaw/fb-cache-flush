# Flush the Facebook Cache for every pate in the
# using http://www.xml-sitemaps.com/ to generate page site maps.

import os
import glob
# If you want to set a timeout for the requests import time
# import time
import urllib
import requests
import xml.etree.ElementTree as ET

# Social URLs + UTMs


def tag_uri_and_name(elem):
    if elem.tag[0] == "{":
        uri, ignore, tag = elem.tag[1:].partition("}")
    else:
        uri = None
        tag = elem.tag
    return uri, tag


# Facebooks Debugger URL
fb_url = "https://developers.facebook.com/tools/debug/og/object"

# Sets user agent
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:16.0) Gecko/20100101 Firefox/16.0"

# ET._namespace_map["http://www.w3.org/2001/XMLSchema-instance"] = 'xsi'

# Declairs the required array for storing files & sitemap page URLs
files = []
all_pages = []

# Loops through all XML files in specified directory
# Loads the XML

# Get all sitemap files and names
os.chdir("sitemaps")
for file in glob.glob("*.xml"):
    files.append(file)


# Loops through all of the sitemap files in the directory
for file in files:
    path = 'sitemaps/' + file
    tree = ET.parse(file)
    root = tree.getroot()

    # gets the XML namespace from the file
    uri, tag = tag_uri_and_name(root)

    if (uri):
        uri = '{' + uri + '}'
        url_namespace = uri + 'url'
        loc_namespace = uri + 'loc'
    else:
        url_namespace = 'url'
        loc_namespace = 'loc'

    # Gets all of the URLs in each sitemap xml file
    # for url in root.findall('url'):
    for url in root.findall(url_namespace):
        for loc in url.findall(loc_namespace):
            url = loc.text

            # This sorts the fields alphabetically, so not good for generating custom URLS for submitting to Facebook
            # paramaters = {
            #     # 'q': escaped_url,
            #     'utm_source': 'source_name',
            #     'utm_medium': 'medium_name',
            #     'utm_campaign': 'campaign_name'
            # }

            paramaters = urllib.urlencode([('utm_source', 'source_name'), ('utm_medium', 'medium_name'), ('utm_campaign', 'campaign_name')])

            # use for an object payload not array
            # payload = url + "?" + urllib.quote(urllib.urlencode(paramaters), '')
            payload = url + "?" + urllib.quote(paramaters, '')

            all_pages.append(payload)


count = 0
while (count < len(all_pages)):
    #If you want to add a timeout while requesting the debugger
    # time.sleep(0.1)

    # Full URL request including FB debugger and params

    full_url = fb_url + "?q=" + all_pages[count]
    r = requests.get(full_url, headers=headers)

    # use if payload is in an object & param order doesn't matter
    # r = requests.get(full_url, params=payload)

    print r.status_code
    print r.url
    print "-----------------"
    count += 1
