# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scrapy.utils.test import get_crawler
from scrapy_tdd import *
from scrapy.selector import Selector
import pytest

from spider import ApiSwaggerSpider

import os


def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)

config_file = os.path.join(my_path(__file__), '..', 'config', 'github_xpath.py')

def describe_swagger_spider_1():    
    to_test = ApiSwaggerSpider.from_crawler(get_crawler(), config_file=config_file)

    def describe_docs_page_1():
        resp = response_from("GitHub API v3 _ GitHub Developer Guide.html")
        results = to_test.parse_api_docs(resp)

        def should_return_other_api_docs():
            # parse results should hold only one item (sometimes parsers have to return a mix!)
            assert count_requests_in_parse_result(results) == 105
            assert count_items_in_parse_result(results) == 0

            urls = urls_from_requests(results)
            assert count_urls_with("/v3/", urls) == 101
