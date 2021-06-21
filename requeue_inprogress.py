#!/usr/bin/env python

from usp.log import create_logger
import redis
import os

log = create_logger(__name__)


r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"))

r.rename("inprogress", "requeue_temp2")

while True:
    v = r.lpop("requeue_temp2")
    if v:
        log.info("Requeueing %s..." % v)
        r.lpush("todo", v)
    else:
        break

