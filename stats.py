#!/usr/bin/env python

from usp.log import create_logger
import redis
import os

log = create_logger(__name__)


r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"))

lists = ["todo", "inprogress"]
sets = ["urls", "enqueued_sitemaps", "valid_sitemaps", "invalid_sitemaps"]

for l in lists:
    size = r.llen(l)
    log.info("{: <20}: {: <10} entries".format(l, size))
for s in sets:
    size = r.scard(s)
    log.info("{: <20}: {: <10} entries".format(s, size))


