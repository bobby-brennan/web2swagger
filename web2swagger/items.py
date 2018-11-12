# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import Join, Compose


def remove_duplicates(in_list):
    already_seen = set()
    ret_list = []
    for elem in in_list:
        if not elem in already_seen:
            ret_list.append(elem)
        already_seen.add(elem)
    return ret_list


def strip_strings(in_list):
    return [ re.sub('\s+',' ',s, flags=re.UNICODE).strip() for s in in_list]


def remove_emptys(in_list):
    return filter(len, filter(None, in_list))


class Remove(object):
    def __init__(self, removal_string):
        self.removal_string = removal_string

    def __call__(self, value):
        if len(value) == 0: return value
        return value.replace(self.removal_string, "").strip()


DEFAULT = scrapy.Field(
    output_processor=Compose(
        strip_strings, remove_emptys, remove_duplicates, Join(' ')),
)

LIST = scrapy.Field(
    output_processor=Compose(
        strip_strings, remove_emptys, remove_duplicates, Join('|')),
)


class SwaggerItem(scrapy.Item):
    src = DEFAULT
    body = DEFAULT
