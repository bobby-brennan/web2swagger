# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import pandas as pd
import re
import imp
import json
import logging
from scrapy.selector import Selector
from genson import SchemaBuilder

from web2swagger.helpers.scraper_helpers import remove_unwanted_unicode_chars
from web2swagger.helpers.swagger_helpers import split_separated_json, clean_json_string, fixSchema, extract_schema_definitions, fixSchemaDefinition


class ApiExtractors:

    def getFirstSelectorTextExtractor(self, selector, extractor):
        if not extractor:
            return selector, ''

        if isinstance(extractor, str):
            return selector, extractor

        if extractor.get('sibling'):
            first_sel = self.getFirstSelectorResult(selector, extractor)
            new_extractor = {}
            if first_sel and extractor:
                new_extractor.update(extractor)
                new_extractor['selector'] = ' '
        else:
            first_sel = selector
            new_extractor = extractor
        return first_sel, new_extractor or extractor

    def getFirstSelectorResult(self, selector, extractor):
        if not extractor:
            return

        if isinstance(extractor, str):
            return extractor

        selectors = self.extractExtractorResults(selector, extractor)
        if selectors:
            return selectors[0]

    def resolveSelector(self, extractor):
        if not extractor:
            return

        if isinstance(extractor, str):
            return extractor

        sel_xpath = extractor.get('selector')

        type = self.resolveExtractorType(extractor)
        if type == 'css':
            if extractor.get('sibling') and not sel_xpath.startswith('* ~'):
                sel_xpath = '* ~ ' + sel_xpath
        else:
            if extractor.get('sibling'):
                if not extractor.get('selector').startswith('./following-sibling::'):
                    sel_xpath = './following-sibling::' + extractor.get('selector').replace(".//", "").strip()
            
        extractor['selector'] = sel_xpath
        return extractor

    def resolveExtractorType(self, extractor):
        return extractor.get('type', self.config.get('type', 'css'))

    def extractExtractorResults(self, selector, extractor):
        if not extractor:
            return

        selectors = []
        if isinstance(extractor, list):
            for ex in extractor:
                selectors += self._extractExtractorSelectorResults(selector, ex)
        else:
            selectors = self._extractExtractorSelectorResults(selector, extractor)

        return selectors

    def _extractExtractorSelectorResults(self, selector, extractor):
        selectors = self.extractSelectorResults(selector, extractor.get('selector'), self.resolveExtractorType(extractor))

        if extractor.get('split'):
            count = 0
            main_data = selector.extract()

            sub_selectors_text = []
            for sel in selectors:
                count += 1
                start_data = sel.extract()
                selector_data = start_data

                if count < len(selectors):
                    next_data = selectors[count].extract()
                    main_to_end_data = main_data.split(next_data)[0]
                    splits = main_to_end_data.split(start_data)
                    between_to_end_data = ''
                    if len(splits) > 1:
                        between_to_end_data = splits[1]
                    if between_to_end_data:
                        selector_data += between_to_end_data
                    sub_selectors_text.append(selector_data)
                else:
                    between_to_end_data = ''
                    splits = main_data.split(selector_data)
                    if len(splits) > 1:
                        between_to_end_data = splits[1]
                    if between_to_end_data:
                        selector_data += between_to_end_data
                    sub_selectors_text.append(selector_data)

            selectors = [Selector(text=x) for x in sub_selectors_text]
        return selectors

    def extractSelectorResults(self, selector, path, type='css'):
        if not type:
            type = 'css'

        if type == 'css':
            try:
                results = selector.css(path)
            except:
                print 'ERROR here: ', selector
                print 'with a css path: ',  path
        else:
            try:
                results = selector.xpath(path)
            except:
                print 'ERROR here: ', selector
                print 'with a xpath path: ',  path
        return results

    def extractText(self, response, extractor):
        if not response:
            return ''

        if not extractor:
            return ''

        if isinstance(extractor, str):
            return extractor

        text = ''
        text_path = extractor.get('selector')
        values = []
        if text_path:
            if self.resolveExtractorType(extractor) == 'css':
                if text_path == ' ':
                    text_path = text_path.strip()

                if not text_path.endswith('text'):
                    text_path = text_path + ' *::text'
                selectors = self.extractSelectorResults(response, text_path, 'css')
            else:                
                if not text_path.endswith('text()'):
                    if text_path == ' ':
                        text_path = text_path.strip()
                        text_path = './/text()'

                    selectors = self.extractSelectorResults(response, text_path, 'xpath')
                else:
                    selectors = self.extractExtractorResults(response, extractor)

            for sel in selectors:
                text = sel.extract()
                text = remove_unwanted_unicode_chars(text)

                if extractor.get('regex'):
                    found = re.search(extractor.get('regex'), text, flags=re.UNICODE)
                    if found:
                        text = found.group(extractor.get('regexMatch', 1))
                        values.append(text)
                else:
                    values.append(text)

            text = extractor.get('join', ' ').join(values)

        text = re.sub('\s+',' ',text, flags=re.UNICODE).strip() or ''

        if not text and extractor.get('default'):
            text = extractor.get('default')

        return text

    def extractInt(self, selector, extractor):
        text = self.extractText(selector, extractor)
        if text:
            return int(text)

    def extractJSON(self, selector, extractor, path='', key='', method=''):
        text = self.extractText(selector, extractor)
        if text and '{' in text and '}' in text:
            json_data = self._validate_json_to_schema(extractor, text)
            if not json_data:
                json_strings = split_separated_json(text)
                if len(json_strings) == 1:
                    json_data = self._validate_json_to_schema(extractor, json_strings[0])
                else:
                    valid_schemas = []
                    for json_text in json_strings:
                        valid_schema = self._validate_json_to_schema(extractor, json_text)
                        if valid_schema:
                            valid_schemas.append(valid_schema)

                    if valid_schemas:
                        json_data = {'anyOf': valid_schemas}

            return json_data or text

    def _validate_json_to_schema(self, extractor, text):
        json_data = None

        try:
            json_string = clean_json_string(text)
            json_data = json.loads(json_string)
        except Exception as e:
            logging.warning('Error converting text to json: %s' % text)
            pass

        if extractor.get('isExample') and json_data:
            json_data = self.json_to_schema(json_data)
        else:
            if json_data:
                json_data = fixSchema(json_data)
                json_data = fixSchemaDefinition(json_data)

        if getattr(self.config_module, "fixPathSchema", None):
            json_data = self.config_module.fixPathSchema(json_data)

        if json_data:
            self.definitions.update(extract_schema_definitions(json_data))

        return json_data

    def json_to_schema(self, json_data):
        json_builder = SchemaBuilder()
        json_builder.add_object(json_data)
        json_data = json_builder.to_schema()
        json_data = fixSchema(json_data)
        if json_data.get('anyOf'):
            for x in json_data.get('anyOf'):
                if 'items' in x:
                    schema_items = x
                    break
            if schema_items:
                json_data.pop('anyOf', None)
                json_data.update(schema_items)
        return json_data

    def extractBoolean(self, selector, extractor, boolean_text=''):
        text = self.extractText(selector, extractor)
        if not text:
            return False

        text = text.lower()
        if boolean_text:
            if boolean_text in text:
                return True
            else:
                return False

        if text == 'false' or text == 'no':
            return False

        return True
