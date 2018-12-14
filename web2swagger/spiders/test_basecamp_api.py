# -*- coding: utf-8 -*-
import pytest
from scrapy_tdd import *
from scrapy.selector import Selector

from api_swagger import ApiSwagger


def response_from(file_name, encoding="latin"):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name, encoding=encoding)

def describe_basecamp_apiswagger():
    config_file = os.path.join(my_path(__file__), '..', 'config', 'basecamp.py')

    to_test = ApiSwagger(config_file=config_file)

    def describe_docs_page_1():
        resp = response_from('bc3-api_campfires.md · GitHub.html')
        result = to_test.parse_paths(resp)

        def should_collect_number_of_paths():
            assert len(result) == 4

        def should_contain_apis():
            assert '/chats.json' in result
            assert '/buckets/{bucketId}/chats/{chatId}.json' in result
            assert '/buckets/{bucketId}/chats/{chatId}/lines.json' in result
            assert '/buckets/{bucketId}/chats/{chatId}/lines/{lineId}.json' in result

        def should_update_existsing_api_with_operation():
            assert 'get' in result['/buckets/{bucketId}/chats/{chatId}/lines.json']
            assert 'post' in result['/buckets/{bucketId}/chats/{chatId}/lines.json']

            assert 'get' in result['/buckets/{bucketId}/chats/{chatId}/lines/{lineId}.json']
            assert 'delete' in result['/buckets/{bucketId}/chats/{chatId}/lines/{lineId}.json']

        def should_parse_paths_response_with_default_status():
            get_item = result['/buckets/{bucketId}/chats/{chatId}/lines.json']['get']
            assert get_item['responses']['200'] == {'description': '', 'schema': {'items': {'type': 'object', 'properties': {u'status': {'type': 'string'}, u'app_url': {'type': 'string'}, u'parent': {'type': 'object', 'properties': {u'url': {'type': 'string'}, u'app_url': {'type': 'string'}, u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'title': {'type': 'string'}}}, u'title': {'type': 'string'}, u'url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'creator': {'type': 'object', 'properties': {u'attachable_sgid': {'type': 'string'}, u'bio': {'type': 'null'}, u'name': {'type': 'string'}, u'title': {'type': 'string'}, u'admin': {'type': 'boolean'}, u'created_at': {'type': 'string'}, u'updated_at': {'type': 'string'}, u'time_zone': {'type': 'string'}, u'avatar_url': {'type': 'string'}, u'personable_type': {'type': 'string'}, u'owner': {'type': 'boolean'}, u'email_address': {'type': 'string'}, u'id': {'type': 'integer'}}}, u'bucket': {'type': 'object', 'properties': {u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'updated_at': {'type': 'string'}, u'id': {'type': 'integer'}, u'content': {'type': 'string'}, u'type': {'type': 'string'}, u'inherits_status': {'type': 'boolean'}, u'bookmark_url': {'type': 'string'}}}, 'type': 'array'}}
            
        def should_strip_empty_spaces_of_json_key_and_values():
            get_item = result['/buckets/{bucketId}/chats/{chatId}.json']['get']
            assert get_item['responses']['200']['schema'] == {'type': 'object', 'properties': {u'status': {'type': 'string'}, u'app_url': {'type': 'string'}, u'title': {'type': 'string'}, u'url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'creator': {'type': 'object', 'properties': {u'attachable_sgid': {'type': 'string'}, u'bio': {'type': 'string'}, u'name': {'type': 'string'}, u'title': {'type': 'string'}, u'admin': {'type': 'boolean'}, u'created_at': {'type': 'string'}, u'updated_at': {'type': 'string'}, u'time_zone': {'type': 'string'}, u'company': {'type': 'object', 'properties': {u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'avatar_url': {'type': 'string'}, u'personable_type': {'type': 'string'}, u'owner': {'type': 'boolean'}, u'email_address': {'type': 'string'}, u'id': {'type': 'integer'}}}, u'bucket': {'type': 'object', 'properties': {u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'updated_at': {'type': 'string'}, u'lines_url': {'type': 'string'}, u'id': {'type': 'integer'}, u'topic': {'type': 'string'}, u'position': {'type': 'integer'}, u'type': {'type': 'string'}, u'inherits_status': {'type': 'boolean'}, u'bookmark_url': {'type': 'string'}}}

        def should_return_security_definitions():
            to_test.parse_apis_info(resp)
            assert to_test.swagger['securityDefinitions']['ApiKeyAuth'] =={'type': 'apiKey','in': 'header','name': 'ACCESS_TOKEN', 'description': "a bearer token, including the prefix 'Bearer', e.g. 'Bearer abcde'"}
            assert to_test.swagger['securityDefinitions']['OAuth 2'] == {'flow': 'accessCode', 'tokenUrl': 'https://launchpad.37signals.com/authorization/token?type=web_server', 'type': 'oauth2', 'authorizationUrl': 'https://launchpad.37signals.com/authorization/new?type=web_server'}

    def describe_docs_page_2():
        resp = response_from('bc3-api_documents_templates.html')
        result = to_test.parse_paths(resp)

        def should_convert_path_to_swagger_path_format():
            assert '/templates/{template_id}/project_constructions.json' in result
            assert '/templates/:template_id/project_constructions.json' not in result

        def should_have_default_response_for_unknown():
            endpoint = result['/templates/{templateId}/project_constructions/{project_constructionId}.json']
            operation = endpoint['get']
            
            assert operation['responses'] == {'200': {'description': 'Unknown'}}
            print operation['parameters']
            assert len([x for x in operation['parameters'] if x['name'] == 'project_constructionId']) == 1
            assert len([x for x in operation['parameters'] if x['name'] == 'templateId']) == 1

    def describe_schemas():
        resp = response_from('basecamp_todolistgroups.html')
        result = to_test.parse_paths(resp)

        endpoint = result['/buckets/{bucketId}/todolists/{todolistId}/groups.json']
        operation = endpoint['post']

        def it_should_return_valid_schema_that_has_separated_json():
            assert operation['responses']['201']['description'] == 'Created'
            assert operation['responses']['201']['schema'] == {'type': 'object', 'properties': {u'name': {'type': 'string'}}}
        
        def it_should_not_contain_an_attribute_required():
            assert 'required' not in operation['responses']['201']['schema']

    def describe_parameters():
        resp = response_from('bc3-api_documents_templates.html')
        result = to_test.parse_paths(resp)

        def it_should_also_contain_parameters_from_path():
            endpoint = result['/templates/{template_id}/project_constructions.json']
            operation = endpoint['post']

            assert len(operation['parameters']) == 2
            assert len([x for x in operation['parameters'] if x['name'] == 'template_id']) == 1

        def it_should_not_include_file_type_of_a_name():
            endpoint = result['/templates/{templateId}.json']
            operation = endpoint['get']

            assert len(operation['parameters']) == 1
            assert len([x for x in operation['parameters'] if x['name'] == 'templateId']) == 1

    def describe_proper_paths():
        resp = response_from('bc3-api_chatbots.html')
        result = to_test.parse_paths(resp)

        def should_convert_chatbot_key_to_chatbotkey():
            assert '/integrations/chatbotKey/buckets/{bucketId}/chats/{chatId}/lines.json' in result
