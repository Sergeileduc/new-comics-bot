#!/usr/bin/python3
# -*-coding:utf-8 -*-

import re
from urllib.parse import parse_qs, urlparse
# from utils.post import Post


# Parse url and get fields
def get_query_field(url, field):
    """Parse url and returns value for key (field)."""
    try:
        return parse_qs(urlparse(url).query)[field]
    except KeyError:
        return []
