# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from openapi_spec_validator import openapi_v2_spec_validator, openapi_v3_spec_validator

import pandas as pd
import re
import imp
import json
import logging
from web2swagger.helpers.generic_file_operations import create_directory_path

from web2swagger.items import SwaggerItem
from api_swagger import ApiSwagger

dir_path = os.path.dirname(os.path.realpath(__file__))
default_config_file = os.path.join(dir_path, '..', 'config', 'github_back_to_back.py')

class ApiSwaggerSpider(CrawlSpider):
    name = "web2swagger"
    start_urls = ()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ApiSwaggerSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.on_spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def on_spider_closed(self, reason):
        generated_specs = self.swagger_app.get_results()
        self._write_out(generated_specs)

        validation_results = self._validate_specs(generated_specs)
        self._write_out(str(validation_results), "validation_results.json")        
    
    def _validate_specs(self, generated_specs):
        try:
            validator = self._pick_validator(generated_specs)
            validation_results = [x for x in validator.iter_errors(generated_specs)]
            actual_validation_messages = 0
            for idx, validation_result in enumerate(validation_results):
                if not self._filter_validation_message(validation_result):
                    logging.warning("%d - %s" % (idx, str(validation_result)))
                    actual_validation_messages += 1
            logging.warning("there were %d (%d) swagger / openapi validation errors" % (actual_validation_messages, len(validation_results)))
            return validation_results
        except:
            logging.error("validation crashed")
            return []

    def _pick_validator(self, specs):
        if str(specs.get("swagger")) == "2.0":
            logging.info("validating against Swagger 2.0")
            return openapi_v2_spec_validator
        else:
            logging.info("validating against OpenAPI 3.0")
            return openapi_v3_spec_validator

    def _filter_validation_message(self, validation_message):
        as_str = str(validation_message)
        return "Failed validating 'oneOf" in as_str or "Failed validating 'anyOf" in as_str or "'anyOf':" in as_str

    def _write_out(self, generated_specs, target_name='specs.json'):
        filepath = self.settings.get('FEED_URI', target_name)
        with open(filepath, 'w') as outfile:
            json.dump(generated_specs, outfile, indent=4)

    def __init__(self, config_file=default_config_file, *args, **kwargs):
        super(ApiSwaggerSpider, self).__init__(*args, **kwargs)
        self.swagger_app = ApiSwagger(config_file=config_file)

    def start_requests(self):
        return [Request(#"file:///data/projects/api2swagger/web2swagger/spiders/samples/JIRA 6.1 REST API documentation.html", 
                        self.swagger_app.config.get('url'), 
                        callback=self.parse_api_docs)]

    def parse_api_docs(self, response):
        self.swagger_app.parse_basic_info(response)
        return self.parse_to_swagger(response)

    def parse_next_docs_page_requests(self, response):
        requests = []

        urls = self.swagger_app.parse_api_urls(response)
        for url in urls:
            requests.append(Request(url, callback=self.parse_to_swagger))

        return requests

    def parse_to_swagger(self, response):
        logging.info("Parsing documentation page %s" % response.url)
        self.swagger_app.parse_apis_info(response)
        return self.parse_next_docs_page_requests(response)
