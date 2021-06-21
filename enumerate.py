#!/usr/bin/env python

from usp.tree import sitemap_tree_for_homepage
from usp.fetch_parse import SitemapFetcher
from usp.objects.sitemap import AbstractSitemap, InvalidSitemap, IndexWebsiteSitemap, IndexRobotsTxtSitemap
import usp
from usp.log import create_logger
import redis
import logging
import os

log = create_logger(__name__)

def fetch_single_sitemap(unpublished_sitemap_url):
    unpublished_sitemap_fetcher = SitemapFetcher(
                url=unpublished_sitemap_url,
                web_client=None,
                recursion_level=10,
    )
    unpublished_sitemap = unpublished_sitemap_fetcher.sitemap()
    return unpublished_sitemap

def enqueue_url(url):
    if not r.sismember('enqueued_sitemaps', url):
        r.sadd("enqueued_sitemaps", url)
        r.lpush("todo", url)

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"))
while True:
    log.info("Waiting for url...")
    response = r.brpoplpush('todo', 'inprogress', timeout=10)
    if response:
        url = response.decode("UTF-8")
        log.info("Got url: %s" % url)
        sm = fetch_single_sitemap(url)
        if not isinstance(sm, InvalidSitemap):
            r.sadd('valid_sitemaps', url)
            if isinstance(sm, usp.objects.sitemap.AbstractIndexSitemap):
                log.info("Queuing sub-sitemaps...")
                c = 0
                for sub in sm.sub_sitemaps:
                    enqueue_url(sub.url)
                    c = c + 1
                log.info("Queued %d sub-sitemaps." % c)
            else:
                log.info("Queuing urls...")
                c = 0
                for page in sm.all_pages():
                    r.sadd('urls', page.url)
                    c = c + 1
                log.info("Queued %d urls." % c)
        else:
            log.warning("Invalid sitemap.")
            r.sadd("invalid_sitemaps", url)
        log.info("Item done, removing from inprogress.")
        r.lrem('inprogress', 1, url)


