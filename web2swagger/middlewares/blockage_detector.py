#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import re
import logging
import time

import scrapy
import codecs


_captcha_text_indicators = (r'/recaptcha/', r'/captcha/', r'g-recaptcha')
_captcha_url_indicators = ['captcha']

_blocked_text_indicators = (r'blocked')
_blocked_http_response_codes = [403, 500]


class BlockageDetectorMiddleware():

    def __init__(self, settings):
        self.output_directory = settings.get('DETECTED_BLOCKAGE_FILES_DIRECTORY', '.')

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def process_response(self, request, response, spider):
        has_detected = False

        if self.find_captcha(response):
            logging.warn('Captcha detected on url ' + response.url)
            self.save_detected_html(response, 'captcha')
            return

        if self.find_blocked(response):
            logging.warn('Block detected on url ' + response.url)
            self.save_detected_html(response, 'blocked')
            return

        return response


    def find_blocked(self, response):
        if response.status in _blocked_http_response_codes:
            return True
        #for blocked_text_indicator in _blocked_text_indicators:
        #    for

    def find_captcha(self, response):
        for url_indicator in _captcha_url_indicators:
            if url_indicator in response.url:
                return True
        captcha_form = response.xpath('.//form').extract()
        text = ''.join(captcha_form).lower().strip()
        for regex in _captcha_text_indicators:
            if self.is_found(regex, text):
                return True
        return False

    def is_found(self, regex, text):
        found = re.compile(regex).findall(text)
        if found:
            return True
        return False

    def save_detected_html(self, response, type):
        if self.output_directory is None:
            return

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        url_name = response.url.replace("/", "_").replace(".", "_").replace(":", "_")
        file_name = '{type}_{name}_{timestamp}.html'.format(type=type, name=url_name, timestamp=time.time())

        storage_path = os.path.join(self.output_directory, file_name)
        try:
            with codecs.open(storage_path, 'w', "utf-8") as file_:
                file_.write(response.text)
        except:
            with codecs.open(storage_path, 'w', "utf-8") as file_:
                file_.write(response.body)

        return storage_path
