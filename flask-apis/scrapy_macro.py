"""Defined Macros to Operate Image Scraper-related Operations
"""


import os


SCRAPER_NODE_IP = os.getenv("SCRAPER_NODE_IP")
SCRAPER_NODE_PORT = os.getenv("SCRAPER_NODE_PORT")

assert SCRAPER_NODE_IP is not None, "`SCRAPER_NODE_IP` Environment Variable is `None`."
assert SCRAPER_NODE_PORT is not None, "`SCRAPER_NODE_PORT` Environment Variable is `None`."
