#!/usr/bin/env python

from usp.log import create_logger
import redis
import os

log = create_logger(__name__)

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"))

r.rename("invalid_sitemaps", "requeue_temp")

while True:
    v = r.spop("requeue_temp", 1)
    if len(v) > 0:
        v = v[0]
        log.info("Requeueing %s..." % v)
        r.lpush("todo", v)
    else:
        break

