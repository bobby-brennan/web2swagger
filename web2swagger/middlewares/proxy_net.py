# -*- coding: utf-8 -*-
from future.standard_library import install_aliases
install_aliases()

import re
import random
import base64
import logging
from urllib.request import urlopen
from twisted.internet import reactor
from collections import OrderedDict
import hashlib
import sys

# TODO:
# factor out blockage detection ... into separate middleware ... that communicates through meta with this middleware

class ProxyNetMiddleware(object):

    def __init__(self, settings):
        logging.info("activating random proxy middleware")
        self.max_retry_times = int(settings.get('RETRY_TIMES', 10))
        self.rotation_strategy= settings.get('PROXY_LIST_STRATEGY', "random") # alternatively round_robin, smart
        self.static_proxy_list = settings.get('PROXY_LIST_STATIC', [])
        self.drop_failed_proxies = settings.get('PROXY_DROP_FAILED', True)
        self.round_robin_counter = 0
        self.proxies = OrderedDict()

        self.proxy_list_url = settings.get('PROXY_LIST_URL', "")
        self.proxy_reload_seconds = settings.get('PROXY_LIST_RELOAD_SECONDS', 1800)
        self._update_proxy_list()
        reactor.callLater(self.proxy_reload_seconds, self.reload_proxy_list)


    def _update_proxy_list(self):
        logging.info("updateing proxy list")
        proxy_list = self._download_proxy_list()
        for line in proxy_list + self.static_proxy_list:
            logging.info(str(line))
            parts = re.match('(\w+:\w+@)?(.+)', line.strip())
            # Cut trailing @
            if parts.group(1):
                user_pass = parts.group(1)[:-1]
            else:
                user_pass = ''
            proxy_address = parts.group(2)
            if "http" not in proxy_address:
                proxy_address = "http://" + proxy_address
            self.proxies[proxy_address] = user_pass

    def _download_proxy_list(self, retries = 5):
        try:
            if retries < 0:   return []
            if self.proxy_list_url == "":    return []
            logging.info("loading proxy list from " + self.proxy_list_url)
            response = urlopen(self.proxy_list_url)
            return response.read().split('\n')
        except:
            return self._download_proxy_list(self, retries - 1)

    def reload_proxy_list(self):
        self._update_proxy_list()
        reactor.callLater(self.proxy_reload_seconds, self.reload_proxy_list)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # print "\n\nprocessing proxy download\n\n"
        if 'dont_proxy' in request.meta:
            logging.info('Proxy disabled for <%s>' % request.url)
            return

        proxy_address = self._choose_proxy(request)
        proxy_user_pass = self.proxies[proxy_address]

        logging.info("Using proxy: " + proxy_address + " out of " + str(len(self.proxies)) + "... for " + request.url)
        request.meta['proxy'] = proxy_address
        request.meta['proxy_details'] = {'server': proxy_address.rsplit(':', 1)[0].replace("http://", '').replace('https://', ''),
                                         'port': proxy_address.rsplit(":", 1)[-1],
                                         'user': proxy_user_pass.split(':')[0],
                                         'password': proxy_user_pass.split(':')[-1]}

        if proxy_user_pass and len(proxy_user_pass) > 0:
            basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth
        else:
            if 'Proxy-Authorization' in request.headers:
                del request.headers['Proxy-Authorization']

    def _choose_proxy(self, request):
        # TODO refactor the strategy into classes
        if len(self.proxies) == 0:
            raise Exception("No Proxies left")
        if 'session' in request.meta:
            proxy_index = int(hashlib.sha1(request.meta['session']).hexdigest(), 16) % len(self.proxies.keys())
            return self.proxies.keys()[proxy_index]
        elif self.rotation_strategy == 'random':
            return random.choice(self.proxies.keys())
        elif self.rotation_strategy == 'round_robin':
            all_keys = self.proxies.keys()
            max = len(all_keys)
            selected = all_keys[self.round_robin_counter % max]
            self.round_robin_counter += 1
            return selected
        else:
            logging.warn("unknown proxy rotation strategy '%s', using 'random' instead" % self.rotation_strategy)
            return random.choice(self.proxies.keys())

    # here's the place to ...
    # ... automatically detect captchas etc ...
    # ... create retries
    # ... shut off bad proxies
    def process_response(self, request, response, spider):
        # print "\n\nprocessing proxy response\n\n"
        #print request
        #print response
        if (self.is_proxy_error(request, response)):
            # mark proxy
            # retry ...
            return self._retry(request, "proxy error", spider)

        if (self.is_target_error(request, response)):
            # mark proxy
            # retry  ...
            return self._retry(request, "target error", spider)

        return response

    def is_proxy_error(self, request, response):
        return False

    def is_target_error(self, request, response):
        # TODO factor this out into a separate service communicating through flags in meta
        # for google
        if "google" in request.url:
            if response.status == 302 and \
                            'location' in response.headers and \
                            "ipv4.google" in response.headers['location']:
                #print "target error: YES\n\n"
                return True
        return False

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        if self.drop_failed_proxies:
            logging.info('Removing failed proxy <%s>, %d proxies left' %
                         (proxy, len(self.proxies)))
            try:
                del self.proxies[proxy]
            except:
                pass
        return self._retry(request, "proxy failed", spider)

    # borrowed from https://github.com/scrapy/scrapy/blob/master/scrapy/downloadermiddlewares/retry.py
    def _retry(self, request, reason = "", spider = None):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            logging.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority
            return retryreq
        else:
            logging.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
