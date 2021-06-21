# Sitemap Enumerator

Based on https://github.com/mediacloud/ultimate-sitemap-parser

This project needs python 3 to be available as `python` on the path. (Can be accomplished with a venv.)

## How to use

First setup a venv with the dependencies and have docker and docker-compose ready.
Adjust the scale in the docker-compose.yml file as desired.
Then run `docker-compose up` to spin up the workers.

Next run `./enqueue.py <url>` to enqueue a site.
Wait until all workers have finished their processing.

Optionally requeue failed using `./requeue_invalid.py` or in-progress (in case a worker crashed at some point) with `./requeue_inprogress.py`.

Finally, extract the info using `./dump.py`.
Under `dump/` you'll find the files.
The `urls.txt` file contains the found urls and the `valid_sitemaps.txt` file contains the urls of the sitemaps themselves.
