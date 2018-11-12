# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from scrapy.utils.test import get_crawler
from scrapy_tdd import *
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import pytest
import sys, os
from jsondiff import diff
import logging
import json

from spiders.spider import ApiSwaggerSpider
from settings import OUTPUT_DIRECTORY
from helpers.generic_file_operations import create_directory_path, save_file, read_json_file

def end_to_end_test(py_config_file, js_config_file, output_file):
    filepath = output_file.split('.json')
    spider_output_file = OUTPUT_DIRECTORY + '/' + filepath[0] + '_spider.json'
    node_output_file = OUTPUT_DIRECTORY + '/' + filepath[0] + '_node.json'

    try:
        os.makedirs(OUTPUT_DIRECTORY)
    except:
        pass

    start_spider(py_config_file, spider_output_file)
    start_node_project(js_config_file, node_output_file)

    node_result = read_json_file(node_output_file)
    spider_result = read_json_file(spider_output_file)

    differences = diff(spider_result, node_result)
    logging.info('Differences will be saved.' )
    save_file(OUTPUT_DIRECTORY, 'difference.json', str(differences))
    

def start_node_project(config_file, output_file):
    logging.info('Start node swagger....')
    print('Start node swagger....')
    os.system("node scrape-to-swagger/node_modules/scrape-to-swagger/index.js --config %s --output %s" % (config_file, output_file))

def start_spider(config_file, output_file):
    logging.info('Start spider....')

    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_URI': output_file,
    })

    process.crawl(ApiSwaggerSpider, config_file=config_file)
    process.start()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        py_config_file = sys.argv[1]
        js_config_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else 'results.json'
        app = end_to_end_test(py_config_file, js_config_file, output_file)
    else:
        raise Exception('Needs config file for spider and npm')

