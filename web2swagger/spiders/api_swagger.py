# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import pandas as pd
import re
import imp
import json
import logging
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from genson import SchemaBuilder

from web2swagger.helpers.scraper_helpers import extract_url_queries, extract_json_dict_child_value, try_regex, remove_unwanted_unicode_chars
from web2swagger.helpers.swagger_helpers import split_separated_json, clean_json_string, convert_to_valid_type, param_default, fixSchema, extract_schema_definitions

# logging.basicConfig(filename='log_1.log',level=logging.DEBUG)

class ApiSwagger:
    swagger = {
        'swagger': "2.0",
        'paths': {},
        'info': {},
        'host': '',
        'basePath': '',
        "securityDefinitions": ""
    }
    api_methods = ['get', 'post', 'patch', 'put', 'delete', 'head', 'options']
    definitions = {}

    def __init__(self, config_file=None):
        if config_file:
            self.load_config(config_file)

    def load_config(self, config_file):
        self.config_module = imp.load_source('module.name', config_file)
        self.config = self.config_module.config

    def get_results(self):
        return self.swagger

    def parse_basic_info(self, response):
        base = ['basePath', 'host']
        info = ['title', 'description', 'version']

        for key in base:
            self.swagger[key] = self.extractText(response, self.config.get(key))

        for key in info:
            self.swagger['info'][key] = self.extractText(response, self.config.get(key))

        self.swagger['schemes'] = self.config.get('schemes') or ['https']

    def parse_apis_info(self, response):
        paths = self.parse_paths(response)
        self.swagger['paths'].update(paths)

        if self.config.get('securityDefinitions'):
            self.swagger['securityDefinitions'] = self.config.get('securityDefinitions')

        if self.definitions:
            self.swagger['definitions'] = self.definitions

    def parse_global_path_attributes(self, response):
        path_global_info = {}
        global_responses = self.parse_responses(response, config=self.config.get('globalExtractors'))
        if global_responses:
            path_global_info['responses'] = global_responses

        global_parameters = self.parse_parameters(response, config=self.config.get('globalExtractors'))
        if global_parameters:
            path_global_info['parameters'] = global_parameters
        return path_global_info

    def parse_paths(self, response):
        if self.config.get('operations'):
            main_operations = self.extractExtractorResults(response, self.config.get('operations'))
        else:
            main_operations = [response]

        operation_data = self.config.get('operation')
        operation_xpath = extract_json_dict_child_value(self.config, ["operation", "selector"])

        paths = {}
        for main_sel in main_operations:
            sub_selectors = self.extractExtractorResults(main_sel, operation_data)
            for sub_sel in sub_selectors:
                op_swag = self.parse_operation(sub_sel)
                for op_path, data in op_swag.items():
                    if op_path in paths:
                        paths[op_path].update(data)
                    else:
                        paths[op_path] = data

        paths = self.add_global_attr_to_paths(response, paths)
        return paths

    def add_global_attr_to_paths(self, response, paths):
        global_path_attr = self.parse_global_path_attributes(response)

        updated_paths = {}
        for path, path_data in paths.items():
            updated_paths[path] = path_data

            if global_path_attr.get('responses') or global_path_attr.get('parameters'):
                for method, data in path_data.items():
                    if global_path_attr.get('responses'):
                        if path_data[method].get('responses') == {'200': {'description': 'Unknown'}}:
                            updated_paths[path][method]['responses'] = global_path_attr.get('responses')
                        else:
                            for stat, global_data in global_path_attr.get('responses').items():
                                if stat in path_data[method]['responses']:
                                    if isinstance(path_data['responses'][stat], dict):
                                        updated_paths[path][method]['responses'][stat] = []
                                        updated_paths[path][method]['responses'][stat].append(path_data[method]['responses'][stat])
                                    updated_paths[path][method]['responses'][stat].append(global_data)
                                else:
                                    updated_paths[path][method]['responses'][stat] = global_data

                    if global_path_attr.get('parameters'):
                        if updated_paths[path][method].get('parameters'):
                            updated_paths[path][method] += global_path_attr['parameters']
                        else:
                            updated_paths[path] = global_path_attr['parameters']

        return updated_paths

    def parse_operation(self, selector):
        operation_swagger = {}
        path = self.extractText(selector, self.config.get('path'))
        if path:
            queries = extract_url_queries(path)
            path = self.config_module.fixPathParameters(path)

            method = self.extractText(selector, self.config.get('method')).lower()
            if method in self.api_methods:
                operation_swagger[path] = {
                    method: {'parameters': [], 'responses': {}}
                }

                # #add operation description
                op_desc = self.extractText(selector, self.config.get('operationDescription'))
                if op_desc:
                    operation_swagger[path][method].update({'description': op_desc})

                #add parameters
                sParameters = self.parse_parameters(selector, path, method, config=self.config)
                self.add_in_path_parameters(path, sParameters)
                if sParameters:
                    operation_swagger[path][method]['parameters'] = sParameters

                #add responses
                path_test = self.extractExtractorResults(selector, self.config['path']).extract()
                dResponses = self.parse_responses(selector, path_test, method, config=self.config)
                operation_swagger[path][method]['responses'] = dResponses if dResponses else {'200': {'description': 'Unknown'}}

        return operation_swagger

    def parse_parameters(self, selector, path='', method='', config={}):
        sParameters = []
        if not config:
            return sParameters        

        bodyParam = self.parse_body_param(selector, config)

        main_parameters = self.extractExtractorResults(selector, config.get('parameters')) or []
        for main_param in main_parameters:
            parameters = self.extractExtractorResults(main_param, config.get('parameter'))
            for param_sel in parameters:
                required = None

                name = self.extractText(param_sel, config.get('parameterName'))
                if self.is_value_exists_in_list_of_dicts(sParameters, 'name', name):
                    continue

                desc = self.extractText(param_sel, config.get('parameterDescription'))
                type, required = self.parse_parameter_type(param_sel, config)

                if config.get('parameterRequired'):
                    required = self.extractBoolean(param_sel, config.get('parameterRequired'))

                in_value = 'query'
                if try_regex('\\{' + name + '\\}', path):
                    in_value = 'path'
                    required = True

                if name:
                    parameter_data = {'name': name, 'type': type.lower(), 'description': desc, 'in': in_value}
                    if required is not None:
                        parameter_data.update({'required': required})
                    sParameters.append(parameter_data)

        if bodyParam:
            sParameters.append(bodyParam)
        return sParameters

    def add_in_path_parameters(self, path, sParameters):
        paths = path.split('/')
        not_found_in_params = []
        for p in paths:
            if '{' in p and '}' in p:
                p = p.replace("{", "").strip()
                p = p.replace("}", "").strip()
                if len([x for x in sParameters if x['name'] == p]) > 0:
                    continue
                else:
                    not_found_in_params.append(p)
        for p in not_found_in_params:
            sParameters.append(param_default(p))
        return sParameters

    def parse_body_param(self, selector, extractor):
        bodyParam = {}
        body_sel = self.getFirstSelectorResult(selector, extractor.get('requestBody'))
        new_extractor = {}
        new_extractor.update(extractor.get('requestBody', {}))
        if body_sel:
            new_extractor['selector'] = ' '
        body = self.extractJSON(body_sel or selector, new_extractor)
        if body:
            bodyParam = {'name': 'body', 'in': 'body'}
            bodyParam['schema'] = body
        return bodyParam

    def parse_parameter_type(self, selector, extractor):
        required = None
        type = self.extractText(selector, extractor.get('parameterType')) or 'string'
        if type.endswith('?'):
            required = False
            type = type.replace("?", "").strip()
        if getattr(self.config_module, "fixParameterType", None):
            type = self.config_module.fixParameterType(type)
        if not type:
            type = 'string'
        type = convert_to_valid_type(type)
        return type, required

    def is_value_exists_in_list_of_dicts(self, list_of_dicts, key, value):
        for x in list_of_dicts:
            if x.get(key) == value:
                return True

        return False

    def parse_responses(self, selector, path='', method='', config={}):
        op_resp = {}
        if not config:
            return op_resp

        stat_config = self.resolveSelector(config.get("responseStatus"))
        desc_config = self.resolveSelector(config.get("responseDescription"))
        schema_config = self.resolveSelector(config.get("responseSchema"))
        responses_sel = self.extractExtractorResults(selector, config.get('responses'))
        status_data = {}

        for response_sel in responses_sel:
            stat = self.parse_response_status(response_sel, stat_config)
            if stat:
                if stat not in status_data:
                    status_data[stat] = []

                response_format = {'description': ""}

                desc_sel, new_desc_config = self.getFirstSelectorTextExtractor(response_sel, desc_config)
                response_format['description'] = self.extractText(desc_sel, new_desc_config)
                schema = self.parse_response_schema(response_sel, schema_config, path)
                if schema:
                    response_format['schema'] = schema

                if response_format not in status_data[stat]:
                    status_data[stat].append(response_format)

        for stat, data in status_data.items():
            if stat in op_resp:
                continue

            op_resp[stat] = data[0]

        return op_resp

    def parse_response_status(self, selector, extractor):
        stat_sel, new_stat_config = self.getFirstSelectorTextExtractor(selector, extractor)
        stat = self.extractText(stat_sel, new_stat_config)
        if 'x' in stat:
            stat = stat.replace('x', '0').strip()
        return stat

    def parse_response_schema(self, selector, extractor, path=''):
        schema = ''
        if not extractor:
            return schema

        schema_sel = self.getFirstSelectorResult(selector, extractor)
        new_schema = {}
        new_schema.update(extractor)
        if schema_sel:
            new_schema['selector'] = ' '
            schema = self.extractJSON(schema_sel, new_schema, path=path) or ''
        return schema

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

    def parse_api_urls(self, response):
        urls = []

        if self.config.get('urlDocsPath'):
            _docs_links = LinkExtractor(
                unique=True,
                restrict_xpaths=('.//a[contains(@href,"%s")][not(contains(@href,"#"))]' % self.config.get('urlDocsPath')))
        else:
            _docs_links = LinkExtractor(allow=(self.config.get('urlRegex')), unique=True)

        for page_link in _docs_links.extract_links(response):
            urls.append(page_link.url)

        return urls

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

    def extractBoolean(self, selector, extractor):
        text = self.extractText(selector, extractor)
        if not text:
            return False

        text = text.lower()
        if text == 'false' or text == 'no':
            return False

        return True