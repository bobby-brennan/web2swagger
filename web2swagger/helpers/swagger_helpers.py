# -*- coding: utf-8 -*-
import json
import re

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
    for key, values in collected_json.items():
        collected_valid_json.append(clean_json_string(' '.join(values).strip()))

    return collected_valid_json

def clean_json_string(json_string):
    json_string = re.sub('"\s+','"',json_string).strip()
    json_string = re.sub('\s+"','"',json_string).strip()
    json_string = re.sub(',\s+}','}',json_string).strip()
    return json_string

def convert_to_valid_type(type):
    type = type.lower()
    valid_type = None
    type_keys = {
        'integer': ['int', 'float', 'decimal'], 
        'boolean': 'bool', 
        'string': 'string'
    }
    for key, ident in type_keys.items():
        if isinstance(ident, list):
            if [x for x in ident if x in type]:
                valid_type = key
                break
        else:
            if key in type or type in key:
                valid_type = key
                break
    if not valid_type:
        valid_type = 'string'
    return valid_type

def param_default(name, required=True, param_in="path", type="string", description=""):
    return {
        "required": required,
        "in": param_in,
        "type": type,
        "name": name, 
        "description": description
    }

def fixSchema(schema):
    if not schema:
        return schema

    schema.pop('$schema', None)
    schema.pop('id', None)

    _remove_none_value(schema)

    return schema

def _remove_none_value(schema):
    if 'required' in schema and not schema['required']:
        schema.pop('required', None)

    for key in schema.get('properties', []):
        _remove_none_value(schema['properties'][key])

    if 'items' in schema:
        _remove_none_value(schema['items'])
    return schema

def extract_schema_definitions(schema):
    definitions = {}

    if 'definitions' in schema:
        definitions = schema.pop('definitions', {})

    return definitions

def fixSchemaDefinition(schema):
    for key, data in schema.get('definitions', {}).items():
        if data.get('type') == 'object' and 'properties' not in data:
            data['type'] = 'string'
    return schema

def is_value_exists_in_list_of_dicts(list_of_dicts, key, value):
    for x in list_of_dicts:
        if x.get(key) == value:
            return True
    return False
