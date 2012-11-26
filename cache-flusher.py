# Flush the Facebook Cache for the pages supplied in the site map(s) located in the sitemaps directory.
# Using http://www.xml-sitemaps.com/ to generate page site maps.

import os
import glob
import time
import urllib
import requests
import xml.etree.ElementTree as ET


class FlushFacebookCache:

    def __init__(self):
        # Facebooks Debugger URL
        self.fb_url = "https://developers.facebook.com/tools/debug/og/object"

        # Sets user agent
        self.headers = {}
        self.headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:16.0) Gecko/20100101 Firefox/16.0"

        # Declairs the required array for storing files & sitemap page URLs
        self.files = []
        self.all_pages = []

        # Delay before next request?
        self.use_timer = False

    def tag_uri_and_name(self, elem):
        if elem.tag[0] == "{":
            uri, ignore, tag = elem.tag[1:].partition("}")
        else:
            uri = None
            tag = elem.tag
        return uri, tag

    def get_files(self):
        # Loops through all XML files in specified directory
        # Get all sitemap files and names
        os.chdir("sitemaps")
        for file in glob.glob("*.xml"):
            self.files.append(file)

        self.get_site_urls()

    def make_request(self):
        count = 0
        while (count < len(self.all_pages)):
            # If you want to add a timeout while requesting the debugger
            if(self.use_timer):
                time.sleep(1.0)

            # Full URL request including FB debugger and params
            full_url = self.fb_url + "?q=" + self.all_pages[count]
            print full_url
            r = requests.get(full_url, headers=self.headers)

            # Use if payload is in an object & param order doesn't matter
            # Comment out above request and uncomment the line below
            # r = requests.get(full_url, params=self.all_pages[count])

            print r.status_code
            print r.url
            print "-----------------"
            count += 1

    def get_site_urls(self):

        # Loops through all of the sitemap files in the directory
        for file in self.files:
            tree = ET.parse(file)
            root = tree.getroot()

            # Gets the XML namespace from the file
            uri, tag = self.tag_uri_and_name(root)

            if (uri):
                uri = '{' + uri + '}'
                url_namespace = uri + 'url'
                loc_namespace = uri + 'loc'
            else:
                url_namespace = 'url'
                loc_namespace = 'loc'

            # Gets all of the URLs in each sitemap xml file
            for url in root.findall(url_namespace):
                for loc in url.findall(loc_namespace):
                    url = loc.text

                    paramaters = urllib.urlencode([('utm_source', 'source_name'), ('utm_medium', 'medium_name'), ('utm_campaign', 'campaign_name')])
                    payload = url + "?" + urllib.quote(paramaters, '')

                    # This sorts the fields alphabetically, so not good for generating custom URLS for submitting to Facebook
                    # Uncomment parameters and other payload below and comment the previous 2 lines if you want to use the object params
                    # paramaters = {
                    #     'utm_source': 'source_name',
                    #     'utm_medium': 'medium_name',
                    #     'utm_campaign': 'campaign_name'
                    # }
                    # Use for an object payload not array
                    # payload = url + "?" + urllib.quote(urllib.urlencode(paramaters), '')

                    self.all_pages.append(payload)

        self.make_request()

flush_cache = FlushFacebookCache()
flush_cache.get_files()
