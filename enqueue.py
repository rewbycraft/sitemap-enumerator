#!/usr/bin/env python
# -*- coding: utf-8 -*-

from usp.exceptions import SitemapException
from usp.fetch_parse import SitemapFetcher
from usp.helpers import is_http_url, strip_url_to_homepage
from usp.log import create_logger
from usp.objects.sitemap import AbstractSitemap, InvalidSitemap, IndexWebsiteSitemap, IndexRobotsTxtSitemap
from usp.web_client.abstract_client import AbstractWebClient
import redis
import sys

log = create_logger(__name__)

r = redis.Redis()

def enqueue_url(url):
    if not r.sismember('enqueued_sitemaps', url):
        r.sadd("enqueued_sitemaps", url)
        r.lpush("todo", url)

_UNPUBLISHED_SITEMAP_PATHS = {
    'sitemap.xml',
    'sitemap.xml.gz',
    'sitemap_index.xml',
    'sitemap-index.xml',
    'sitemap_index.xml.gz',
    'sitemap-index.xml.gz',
    '.sitemap.xml',
    'sitemap',
    'admin/config/search/xmlsitemap',
    'sitemap/sitemap-index.xml',
    'sitemap_news.xml',
    'sitemap-news.xml',
    'sitemap_news.xml.gz',
    'sitemap-news.xml.gz',
}

def enqueue_homepage(homepage_url: str) -> AbstractSitemap:
    """
    Using a homepage URL, fetch the tree of sitemaps and pages listed in them.
    :param homepage_url: Homepage URL of a website to fetch the sitemap tree for, e.g. "http://www.example.com/".
    :param web_client: Web client implementation to use for fetching sitemaps.
    :return: Root sitemap object of the fetched sitemap tree.
    """

    if not is_http_url(homepage_url):
        raise SitemapException("URL {} is not a HTTP(s) URL.".format(homepage_url))

    stripped_homepage_url = strip_url_to_homepage(url=homepage_url)
    if homepage_url != stripped_homepage_url:
        log.warning("Assuming that the homepage of {} is {}".format(homepage_url, stripped_homepage_url))
        homepage_url = stripped_homepage_url

    if not homepage_url.endswith('/'):
        homepage_url += '/'
    robots_txt_url = homepage_url + 'robots.txt'

    sitemaps = []

    enqueue_url(robots_txt_url)

    for unpublished_sitemap_path in _UNPUBLISHED_SITEMAP_PATHS:
        unpublished_sitemap_url = homepage_url + unpublished_sitemap_path
        enqueue_url(unpublished_sitemap_url)


enqueue_homepage(sys.argv[1])
