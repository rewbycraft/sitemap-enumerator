#!/usr/bin/env python

from usp.log import create_logger
import redis
import os

log = create_logger(__name__)


r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"))

lists = ["todo", "inprogress"]
sets = ["urls", "enqueued_sitemaps", "valid_sitemaps", "invalid_sitemaps"]

os.mkdir('dump')

for l in lists:
    log.info("Dumping %s..." % l)
    with open("dump/{}.txt".format(l), 'w') as fh:
        for elem in r.lrange(l, 0, -1):
            fh.write("{}\n".format(elem.decode("UTF-8")))
for s in sets:
    log.info("Dumping %s..." % s)
    with open("dump/{}.txt".format(s), 'w') as fh:
        for elem in r.smembers(s):
            fh.write("{}\n".format(elem.decode("UTF-8")))


