# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import pandas as pd
import re
import imp
import json
import logging

from web2swagger.helpers.scraper_helpers import try_regex
from web2swagger.helpers.swagger_helpers import convert_to_valid_type, param_default, is_value_exists_in_list_of_dicts


class ApiParameters:
    endpoint_formats = ['rpc', 'content-download', 'content-upload']

    def parse_path_parameters(self, selector, path, method, endpoint_format, config={}):
        sParameters = self.parse_parameters(selector, path, method, config=config)
        self.add_in_path_parameters(path, sParameters)
        if sParameters:
            if endpoint_format.lower() in self.endpoint_formats:
                sParameters = self.fixEndPointParameters(sParameters, endpoint_format)

            if getattr(self.config_module, "fixPathParameters", None):
                sParameters = self.config_module.fixPathParameters(sParameters)

        return sParameters

    def fix_all_paths(self, paths):
        self.add_post_parameters_in_put(paths)

    def add_post_parameters_in_put(self, paths):
        path_keys = [path for path, values in paths.items() if 'put' in values]
        for path_key in path_keys:
            post_pair_key = self._find_path_post_pair(path_key, paths)
            if post_pair_key:
                post_params = [post_param for post_param in paths[post_pair_key]['post'].get('parameters') if post_param.get('in') != 'path']
                path_params = paths[path_key]['put'].get('parameters', [])

                for x in post_params:
                    if len([y for y in path_params if y['name'] == x['name']]) == 0:
                        path_params.append(x)

    def _find_path_post_pair(self, path_key, paths):
        path_key_parts = path_key.split('/{')
        if len(path_key_parts) > 1:
            post_pair_key = path_key_parts[0]
            if post_pair_key in paths and 'post' in paths[post_pair_key]:
                return post_pair_key

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

    def fixDescription(self, description):
        if description.lower() == "no description":
            description = ''
        return description

    def fixEndPointParameters(self, parameters, endpoint_format):
        if 'rpc' in endpoint_format.lower():
            fixed_parameters = self.fix_rpc_parameters(parameters)
        elif 'content-download' in endpoint_format.lower():
            fixed_parameters = self._fix_content_parameters(parameters, 'string')
        elif 'content-upload' in endpoint_format.lower():
            fixed_parameters = self._fix_content_parameters(parameters, 'file')    

        if getattr(self.config_module, "fixEndPointParameters", None):
            fixed_parameters = self.config_module.fixEndPointParameters(fixed_parameters, endpoint_format)

        return fixed_parameters

    def _fix_content_parameters(self, parameters, type):
        fixed_parameters = []
        param = {'in': 'header', 'name': self.config.get('title'), 'type': 'string'}

        param_properties = {'properties': []}
        for x in parameters:
            param_properties['properties'].append(x['name'])

        param['description'] = json.dumps(param_properties)

        fixed_parameters.append(param)

        if type == 'file':
            fixed_parameters.append({'in': 'body', 'name': 'file', 'type': type})

        return fixed_parameters

    def fix_rpc_parameters(self, parameters):
        schema = self._merge_parameter_schema(parameters)
        fixed_parameters = []
        for x in parameters:
            if 'schema' not in x:
                if x['in'] == 'body':
                    if not schema:
                        schema = {'schema': {'type': 'object', 'properties': {}}}
                    property_name = x['name']
                    if x.get("required", False):
                        if 'required' not in schema['schema']:
                            schema['schema']['required'] = []
                        if property_name not in schema['schema']['required']:
                            schema['schema']['required'].append(property_name)
                    x.pop('in', None)
                    x.pop('name', None)
                    x.pop('required', None)
                    schema['schema']['properties'][property_name] = x
                else:
                    fixed_parameters.append(x)
        if schema:
            schema.update({'in': 'body', 'name': 'body'})
            fixed_parameters.append(schema)
        return fixed_parameters

    def _merge_parameter_schema(self, parameters):
        schema = {}
        for x in parameters:
            if 'schema' in x:
                if not schema:
                    schema = x
                else:
                    schema['schema']['properties'].update(x['properties'])
        return schema

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
                readonly = None

                name = self.extractText(param_sel, config.get('parameterName'))
                if is_value_exists_in_list_of_dicts(sParameters, 'name', name):
                    continue

                desc = self.extractText(param_sel, config.get('parameterDescription'))
                type, required = self.parse_parameter_type(param_sel, config)

                if config.get('parameterRequired'):
                    required = self.extractBoolean(param_sel, config.get('parameterRequired'), 'required')

                if config.get('parameterReadOnly'):
                    readonly = self.extractBoolean(param_sel, config.get('parameterReadOnly'), 'read-only')

                if try_regex('\\{' + name + '\\}', path):
                    in_value = 'path'
                    required = True
                else:
                    if method in self.parameterLocations:
                        in_value = self.parameterLocations[method]
                    else:
                        in_value = 'formData'

                if name:
                    parameter_data = {'name': name, 'type': type.lower(), 'description': self.fixDescription(desc), 'in': in_value}
                    if required is not None:
                        parameter_data.update({'required': required})

                    if not readonly or (readonly and in_value not in ['formData', 'body']):
                        sParameters.append(parameter_data)

        if bodyParam:
            sParameters.append(bodyParam)
        return sParameters

    def add_in_path_parameters(self, path, sParameters):
        paths = path.split('/')
        not_found_in_params = []
        for p in paths:
            found_name = re.findall(r'{(.*?)}', p, flags=re.UNICODE)
            if found_name:                
                if len([x for x in sParameters if x['name'] == found_name[0]]) > 0:
                    continue
                else:
                    not_found_in_params.append(found_name[0])
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

    def getDefaultParameterLocation(self, config):
        parameterLocations = {}
        for m in self.api_methods:
            if config.get('defaultParameterLocations') and m in config.get('defaultParameterLocations'):
                parameterLocations[m] = config.get('defaultParameterLocations')[m]
                if parameterLocations[m] == 'field':
                    parameterLocations[m] = 'body'
            else:
                if m == 'post' or m == 'patch' or m == 'put':
                    parameterLocations[m] = 'formData'
                else:
                    parameterLocations[m] = 'query'
        return parameterLocations
