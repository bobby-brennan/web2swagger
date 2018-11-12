# -*- coding: utf-8 -*-
import os
import codecs
import hashlib
import logging
import re
import json

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
     from urlparse import urlparse, parse_qs
import urllib


def try_regex(regex, text):
    found = re.findall(regex, text, flags=re.UNICODE)
    if found:
        return True
    return False

def extract_value(selector, path, join_string=" "):
    values = selector.xpath(path).extract()
    if join_string:
        return join_string.join(values).strip()
    return values

def re_extraction_in_between_strings(beg_exp, end_exp, value):
    regular_expresssion = beg_exp + r'(.*?)' + end_exp
    found = re.findall(regular_expresssion, value, flags=re.UNICODE | re.DOTALL )
    if found:
        return found[0].strip()

def extract_json_dict_child_value(json, path):
    while len(path) > 0:
        if json:
            json = json.get(path[0])
            if not json:
                break
        path.pop(0)
    return json

def strip_strings(in_list):
    return [ re.sub('\s+',' ',s, flags = re.UNICODE).strip() for s in in_list]

def get_base_url(url):
    parsed_url = urlparse(url)
    return "https://" + parsed_url.netloc

def complete_url(url):
    if not url.startswith("http"):
        url = "https://" + url
    return url

def build_next_page_url(url, next_page_no):
    nextpage_param = 'page=' + next_page_no

    if 'page=' in url:
        splitted_url = url.split('page=')
        return splitted_url[0] + nextpage_param
    else:
        if '?' in url:
            url = url + '&' + nextpage_param
        else:
            url = url + '?' + nextpage_param
        return url

def extract_url_queries(url, query_key=None):
    parsed = urlparse(url)
    queries = parse_qs(parsed.query)
    if query_key:
        values = queries.get(query_key)
        if values:
            return values[0]
        else:
            return ''
    return queries

bad_chars = {
    u'\xc2\x82' : ',',        # High code comma
    u'\xc2\x84' : ',,',       # High code double comma
    u'\xc2\x85' : '...',      # Tripple dot
    u'\xc2\x88' : '^',        # High carat
    #'\xc2\x91' : '\x27',     # Forward single quote
    #'\xc2\x92' : '\x27',     # Reverse single quote
    #'\xc2\x93' : '\x22',     # Forward double quote
    #'\xc2\x94' : '\x22',     # Reverse double quote
    u'\xc2\x95' : ' ',
    u'\xc2\x96' : '-',        # High hyphen
    u'\xc2\x97' : '--',       # Double hyphen
    u'\xc2\x99' : ' ',
    u'\xc2\xa0' : ' ',
    u'\xc2\xa6' : '|',        # Split vertical bar
    u'\xc2\xab' : '<<',       # Double less than
    u'\xc2\xbb' : '>>',       # Double greater than
    u'\xc2\xbc' : '1/4',      # one quarter
    u'\xc2\xbd' : '1/2',      # one half
    u'\xc2\xbe' : '3/4',      # three quarters
    u'\xca\xbf' : '\x27',     # c-single quote
    u'\xcc\xa8' : '',         # modifier - under curve
    u'\xcc\xb1' : '',          # modifier - under line

    u'\xe2\x80\x80': ' ',
    u'\xe2\x80\x81': ' ',
    u'\xe2\x80\x82': ' ',
    u'\xe2\x80\x83': ' ',
    u'\xe2\x80\x84': ' ',
    u'\xe2\x80\x85': ' ',
    u'\xe2\x80\x86': ' ',
    u'\xe2\x80\x87': ' ',
    u'\xe2\x80\x88': ' ',
    u'\xe2\x80\x89': ' ',
    u'\xe2\x80\x8a': ' ',
    u'\xe2\x80\x8b': ' ',
    u'\xe2\x80\x8c': ' ',
    u'\xe2\x80\x8d': ' ',
    u'\xe2\x80\x8e': ' ',
    u'\xe2\x80\x8f': ' ',


    r'\xc2\x82' : ',',        # High code comma
    r'\xc2\x84' : ',,',       # High code double comma
    r'\xc2\x85' : '...',      # Tripple dot
    r'\xc2\x88' : '^',        # High carat
    #'\xc2\x91' : '\x27',     # Forward single quote
    #'\xc2\x92' : '\x27',     # Reverse single quote
    #'\xc2\x93' : '\x22',     # Forward double quote
    #'\xc2\x94' : '\x22',     # Reverse double quote
    r'\xc2\x95' : ' ',
    r'\xc2\x96' : '-',        # High hyphen
    r'\xc2\x97' : '--',       # Double hyphen
    r'\xc2\x99' : ' ',
    r'\xc2\xa0' : ' ',
    r'\xc2\xa6' : '|',        # Split vertical bar
    r'\xc2\xab' : '<<',       # Double less than
    r'\xc2\xbb' : '>>',       # Double greater than
    r'\xc2\xbc' : '1/4',      # one quarter
    r'\xc2\xbd' : '1/2',      # one half
    r'\xc2\xbe' : '3/4',      # three quarters
    #'\xca\xbf' : '\x27',     # c-single quote
    r'\xcc\xa8' : '',         # modifier - under curve
    r'\xcc\xb1' : '',          # modifier - under line

    r'\xe2\x80\x80': ' ',
    r'\xe2\x80\x81': ' ',
    r'\xe2\x80\x82': ' ',
    r'\xe2\x80\x83': ' ',
    r'\xe2\x80\x84': ' ',
    r'\xe2\x80\x85': ' ',
    r'\xe2\x80\x86': ' ',
    r'\xe2\x80\x87': ' ',
    r'\xe2\x80\x88': ' ',
    r'\xe2\x80\x89': ' ',
    r'\xe2\x80\x8a': ' ',
    r'\xe2\x80\x8b': ' ',
    r'\xe2\x80\x8c': ' ',
    r'\xe2\x80\x8d': ' ',
    r'\xe2\x80\x8e': ' ',
    r'\xe2\x80\x8f': ' ',
}

def remove_unwanted_unicode_chars(unicode):
    try:
        unicode = unicode.replace("&#160;", " ")
        unicode = unicode.replace('&#xd;', " ")
        for bad_char in bad_chars:
            unicode = unicode.replace(bad_char, bad_chars[bad_char])
        for bad_char in bad_chars:
            unicode = unicode.replace(bad_char.replace(u'\xc2', ''), bad_chars[bad_char])
    except:
        pass
    return unicode

def split_separated_json(json_string):
    pieces = json_string.split()
    valid_start_keys = [{'start': '{', 'end': '}'}, {'start': '[', 'end': ']'}]
    valid_next_strings = [']', ',']

    collected_json = {}
    count = 0
    found_json = True        
    key = None
    for index, p in enumerate(pieces):
        p = p.strip()

        if not key:
            for x in valid_start_keys:
                if p.startswith(x['start']):
                    key = x
                    break

        if not key:
            continue

        if found_json:
            if not p.startswith(key['start']):
                continue
            else:
                count += 1
                found_json = False

        if str(count) not in collected_json:
            collected_json[str(count)] = []

        collected_json[str(count)].append(p)

        if p.endswith(key['end']):
            next_enum = index + 2
            if len(pieces) > next_enum:
                next_value = pieces[index+1]
                if [x in next_value for x in valid_next_strings]:
                    found_json = True

    collected_valid_json = []
    # if len(collected_json) == 1:
    #     collected_valid_json.append(json_string)

    # if len(collected_json) > 1:
    for key, values in collected_json.items():
        collected_valid_json.append(clean_json_string(' '.join(values).strip()))

    return collected_valid_json

def clean_json_string(json_string):
    json_string = re.sub('"\s+','"',json_string).strip()
    json_string = re.sub('\s+"','"',json_string).strip()
    json_string = re.sub(',\s+}','}',json_string).strip()
    return json_string
