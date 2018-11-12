# -*- coding: utf-8 -*-
from scrapy.utils.test import get_crawler
from scrapy_tdd import *
import pytest
import os

from scraper_helpers import *

def describe_helpers():
    
    def should_collect_url_queries():
        assert extract_url_queries("foo.appspot.com/abc?def=ghi&userId=jen") == {'def': ['ghi'], 'userId': ['jen']}
