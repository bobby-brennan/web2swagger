# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import pandas as pd
import re
import imp
import json
import logging
from scrapy.linkextractors import LinkExtractor
from genson import SchemaBuilder

from web2swagger.helpers.scraper_helpers import extract_url_queries

from api_parameters import ApiParameters
from api_extractors import ApiExtractors

class ApiSwagger(ApiExtractors, ApiParameters):
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
    endpoint_formats = ['rpc', 'content-download', 'content-upload']

    def __init__(self, config_file=None):
        if config_file:
            self.load_config(config_file)

    def load_config(self, config_file):
        self.config_module = imp.load_source('module.name', config_file)
        self.config = self.config_module.config
        self.parameterLocations = self.getDefaultParameterLocation(self.config)

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

    def parse_paths(self, response):
        if self.config.get('operations'):
            operation_descriptions = self.config.get('operations')
            if isinstance(self.config.get('operations'), dict):
                operation_descriptions = [operation_descriptions]
            main_operations = []
            for op_desc in operation_descriptions:
                main_operations += self.extractExtractorResults(response, op_desc)
        else:
            main_operations = [response]

        paths = {}
        for main_sel in main_operations:
            sub_selectors = self.extractExtractorResults(main_sel, self.config.get('operation'))

            for sub_sel in sub_selectors:
                op_swag = self.parse_operation(sub_sel)
                if getattr(self.config_module, "fixOperationData", None):
                    op_swag = self.config_module.fixOperationData(op_swag)

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
                    self._add_global_responses(path, path_data, global_path_attr, method, updated_paths)
                    self._add_global_parameters(path, path_data, global_path_attr, method, updated_paths)

        return updated_paths

    def _add_global_responses(self, path, path_data, global_path_attr, method, updated_paths):
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

    def _add_global_parameters(self, path, path_data, global_path_attr, method, updated_paths):
        if global_path_attr.get('parameters'):
            if updated_paths[path][method].get('parameters'):
                unduplicated_global_params = []
                for x in global_path_attr['parameters']:
                    if 'schema' not in x:
                        if len([y for y in updated_paths[path][method].get('parameters') if y['name'] == x['name']]) == 0:
                            unduplicated_global_params.append(x)
                    else:
                        unduplicated_global_params.append(x)
                updated_paths[path][method]['parameters'] += unduplicated_global_params
            else:
                updated_paths[path][method]['parameters'] = global_path_attr['parameters']

    def parse_global_path_attributes(self, response):
        path_global_info = {}
        global_responses = self.parse_responses(response, config=self.config.get('globalExtractors'))
        if global_responses:
            path_global_info['responses'] = global_responses

        global_parameters = self.parse_path_parameters(response, '', '', '', config=self.config.get('globalExtractors'))
        if global_parameters:
            path_global_info['parameters'] = global_parameters
        return path_global_info

    def parse_operation(self, selector):
        operation_swagger = {}
        path = self.extractText(selector, self.config.get('path'))
        
        if path:
            queries = extract_url_queries(path)
            path = self.fixPath(path)
            method = self.extractText(selector, self.config.get('method')).lower()
            if method in self.api_methods:
                operation_swagger[path] = {
                    method: {'parameters': [], 'responses': {}}
                }

                endpoint_format = self.extractText(selector, self.config.get('endPointFormat'))

                # #add operation description
                op_desc = self.extractText(selector, self.config.get('operationDescription'))
                if op_desc:
                    operation_swagger[path][method].update({'description': self.fixDescription(op_desc)})

                sParameters = self.parse_path_parameters(selector, path, method, endpoint_format, config=self.config)
                if sParameters:
                    operation_swagger[path][method]['parameters'] = sParameters

                #add responses
                path_test = self.extractExtractorResults(selector, self.config['path']).extract()
                dResponses = self.parse_responses(selector, path_test, method, config=self.config)
                operation_swagger[path][method]['responses'] = dResponses if dResponses else {'200': {'description': 'Unknown'}}

        return operation_swagger

    def fixPath(self, path):
        if getattr(self.config_module, "fixPathString", None):
            path = self.config_module.fixPathString(path)
        # path = self.config_module.fixPathParameters(path)
        if self.config.get('basePath') and not self.config.get('basePath') == '/':
            splitted_path = path.split(self.config.get('basePath'))
            if len(splitted_path) > 1:
                path = ''.join(splitted_path[1:])
        return path

    def parse_responses(self, selector, path='', method='', config={}):
        op_resp = {}
        if not config:
            return op_resp

        stat_config = self.resolveSelector(config.get("responseStatus"))
        desc_config = self.resolveSelector(config.get("responseDescription"))
        schema_config = self.resolveSelector(config.get("responseSchema"))
        responses_sel = self.extractExtractorResults(selector, config.get('responses')) or []
        status_data = {}

        for response_sel in responses_sel:
            stat = self.parse_response_status(response_sel, stat_config)
            if stat:
                if stat not in status_data:
                    status_data[stat] = []

                response_format = {'description': ""}

                desc_sel, new_desc_config = self.getFirstSelectorTextExtractor(response_sel, desc_config)
                response_format['description'] = self.fixDescription(self.extractText(desc_sel, new_desc_config))
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
