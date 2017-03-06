#!/usr/bin/env python


##edited from example code at tornado

import time
from datetime import timedelta
import sqlite3
import re

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues

base_url = 'http://www.breitbart.com'
concurrency = 10
emails =[]
externals = []
internals = []
broken = []

@gen.coroutine
def get_links_from_url(url):
    global internals,emails,externals, broken
    """Download the page at `url` and parse it for links.

    Returned links have had the fragment after `#` removed, and have been made
    absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
    'http://www.tornadoweb.org/en/stable/gen.html'.
    """
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(url)
        if not url in internals:
            internals = internals + [url]
#        print('fetched %s' % url)

        html = response.body if isinstance(response.body, str) \
            else response.body.decode()
        urls = [urljoin(url, remove_fragment(new_url))
                for new_url in get_links(html)]
    except Exception as e:
        if "mailto:" in url:
            if not url in emails:
                emails = emails+[url]
 #           print('Found email %s' %url)
        else:
            if not url in broken:
                broken = broken + [url]
  #          print('Exception: %s %s' % (e, url))
        raise gen.Return([])

    raise gen.Return(urls)


def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get('href')
            if href and tag == 'a':
                self.urls.append(href)
            
    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls


@gen.coroutine
def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()

    @gen.coroutine
    def fetch_url():
        global internals,emails,externals
        current_url = yield q.get()
        try:
            if current_url in fetching:
                return

#            print('fetching %s' % current_url)
            fetching.add(current_url)
            urls = yield get_links_from_url(current_url)
            fetched.add(current_url)

            for new_url in urls:
                # Only follow links beneath the base URL
                strippedbase = base_url.replace("http://","").replace("www.","")
                if strippedbase in new_url:
                    yield q.put(new_url)
                else:
                    if "mailto:" in new_url:
                        if not new_url in emails:
                            emails = emails + [new_url]
                    elif not new_url in externals:
                        externals = externals + [new_url]
                    

        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put(base_url)

    # Start workers, then wait for the work queue to be empty.
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=300))
    assert fetching == fetched
    print('Done in %d seconds, fetched %s URLs.' % (
        time.time() - start, len(fetched)))


def addToDB(cur,friendlyname,item,itemtype):
    cur.execute("REPLACE INTO '" + str(friendlyname) + "' VALUES ('" + str(item) + "', '"+str(itemtype)+"')")

def Run(site,friendlyname):
    global base_url
    base_url = site

    import logging
    logging.basicConfig()
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
    con = sqlite3.connect("Output.db")
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE 'results' ( 'name' TEXT UNIQUE, 'url' TEXT, 'emails' INTEGER, 'externals' INTEGER, 'internals' INTEGER, 'broken' INTEGER, PRIMARY KEY('name') )")
        con.commit()
    except:
        print("results TABLE ALREADY EXISTS?")

    try:
        cur.execute("CREATE TABLE '"+str(friendlyname)+"' ('link' TEXT UNIQUE, 'type' TEXT, PRIMARY KEY('link') )")
        con.commit()
    except:
        print(str(friendlyname) + " TABLE ALREADY EXISTS?")

    for item in emails:
        addToDB(cur,friendlyname,item,"EMAIL")
    for item in externals:
        addToDB(cur,friendlyname,item,"EXTERNAL")
    for item in internals:
        addToDB(cur,friendlyname,item,"INTERNAL")
    for item in broken:
        addToDB(cur,friendlyname,item,"BROKEN")

    con.commit()
    cur.execute("REPLACE INTO 'results' VALUES('"+str(friendlyname)+"','"+str(site)+"',"+str(len(emails))+","+str(len(externals))+","+str(len(internals))+","+str(len(broken))+")")
    con.commit()
    con.close()

