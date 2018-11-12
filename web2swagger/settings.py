# -*- coding: utf-8 -*-

# Scrapy settings for example project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'web2swagger'

SPIDER_MODULES = ['web2swagger.spiders']
NEWSPIDER_MODULE = 'web2swagger.spiders'

OUTPUT_DIRECTORY = './output'

LOG_LEVEL = 'INFO'

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_TIMEOUT = 30

# Autothrottle makes the scraper go es fast as possible (by measuring how fast the target site allows us to go)
# ============
# activate it once the scraper is working well for faster testing and faster results

DOWNLOAD_DELAY = .1 # Autothrottle never goes below this value and so we have to set it to low
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1


DOWNLOADER_MIDDLEWARES = {

    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
}

FEED_FORMAT = 'json'

