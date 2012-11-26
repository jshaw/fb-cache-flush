fb-cache-flush
==============

This script flushs the Facebook Cache used for storing the OG:tags for their Like and Send buttons.
If your page has been cached by Facebook and you have made updates to your OG:tags in your your page header there can be a delay of up to one week+ before the caches are cleared that are used for populating the images, title, description etc... for the the FB like pop up dialog on pages.

This script takes the files and the URLs specified in the sitemap directory and runs each URL through the Facebook Debugger (https://developers.facebook.com/tools/debug).

The option of adding unique paramaters to the requests per URL is also availabble. In the original use case it was to target Google Analytics UTM codes appended to the URL.

This is best used for sites with a large URL tree and possibly unique URLs per language etc.

At the moment you need to generate the sitemaps manually.
The sitemaps are generated using http://www.xml-sitemaps.com.
