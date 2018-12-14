# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scrapy.utils.test import get_crawler
from scrapy_tdd import *
from scrapy.selector import Selector
import pytest
import json
import logging

from spider import ApiSwaggerSpider

import os

def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)

config_file = os.path.join(my_path(__file__), '..', 'config', 'confluence.py')

def describe_swagger_spider_1():    
    to_test = ApiSwaggerSpider.from_crawler(get_crawler(), config_file=config_file)

    def describe_docs_page_1():
        resp = response_from("confluence.html")
        results = to_test.swagger_app.parse_paths(resp)

        def should_collect_number_of_paths():
            assert len(results) == 47

        def should_contain_apis():
            assert '/content/{id}/restriction/byOperation' in results
            assert '/user/watch/content/{contentId}' in results
            assert '/space/{spaceKey}/property/{key}' in results
            assert '/accessmode' in results
            assert '/content' in results

        def should_not_exists_in_apis():
            assert '/content/{id}/riction/byOperation' not in results

        def should_update_existsing_api_with_operation():
            assert 'get' in results['/audit/retention']
            assert 'put' in results['/audit/retention']

            assert 'get' in results['/content/{id}/property/{key}']
            assert 'put' in results['/content/{id}/property/{key}']
            assert 'delete' in results['/content/{id}/property/{key}']
            assert 'post' in results['/content/{id}/property/{key}']

        def should_return_swagger_path_with_bracket_and_with_many_methods_and_responses():
            post_item = results['/user/watch/content/{contentId}']['post']
            assert post_item['responses']['404']['description'] == u'Returned if no content exists for the specified content id or the calling user does not have permission to perform the operation'
            assert post_item['responses']['204']['description'] == u'application/json Returned if the watcher was successfully created'
            assert post_item['parameters'] == [{'in': 'formData', 'type': u'string', 'name': u'key', 'description': u'userkey of the user to create the new watcher for'}, {'in': 'formData', 'type': u'string', 'name': u'username', 'description': u'username of the user to create the new watcher for'}, {'required': True, 'in': 'path', 'name': 'contentId', 'description': '', 'type': 'string'}]

            get_item = results['/user/watch/content/{contentId}']['get']
            assert get_item['responses']['200'] == {'description': u'application/json Returns a JSON representation containing the watching state'}
            assert get_item['responses']['404'] == {'description': u'Returned if no content exists for the specified content id or calling user does not have permission to perform the operation'}
            assert get_item['parameters'] == [{'in': 'query', 'type': u'string', 'name': u'key', 'description': u'userkey of the user to check for watching state'}, {'in': 'query', 'type': u'string', 'name': u'username', 'description': u'username of the user to check for watching state'}, {'required': True, 'in': 'path', 'name': 'contentId', 'description': '', 'type': 'string'}]

            del_item = results['/user/watch/content/{contentId}']['delete']
            assert del_item['responses']['204'] == {'description': u'application/json Returned if the watcher was successfully deleted'}
            assert del_item['responses']['404'] == {'description': u'Returned if no content exists for the specified content id or the calling user does not have permission to perform the operation'}
            assert del_item['parameters'] == [{'in': 'query', 'type': u'string', 'name': u'key', 'description': u'userkey of the user to delete the watcher for'}, {'in': 'query', 'type': u'string', 'name': u'username', 'description': u'username of the user to delete the watcher for'}, {'required': True, 'in': 'path', 'name': 'contentId', 'description': '', 'type': 'string'}]
        
        def should_return_path_with_no_bracket_and_no_responses():
            item = results['/audit']['post']
            assert item['responses'] == {'200': {'description': 'Unknown'}}

            item = results['/audit']['get']
            assert item['responses'] == {'200': {'description': 'Unknown'}}
            assert item['parameters'] == [{'in': 'query', 'type': u'string', 'name': u'startDate', 'description': ''}, {'in': 'query', 'type': u'string', 'name': u'endDate', 'description': ''}, {'in': 'query', 'type': u'integer', 'name': u'start', 'description': u'where to start within results set'}, {'in': 'query', 'type': u'integer', 'name': u'limit', 'description': u'the maximum results to fetch'}, {'in': 'query', 'type': u'string', 'name': u'searchString', 'description': ''}]

        def describe_parameters():

            def should_convert_int_to_integer():
                endpoint = results['/content/{id}/property']
                operation = endpoint['get']

                assert operation['parameters'][1]["type"] == "integer"

            def should_add_in_parameters_that_has_no_set_parameters():
                endpoint = results['/content/{id}/history/{version}/macro/hash/{hash}']
                operation = endpoint['get']

                assert len(operation['parameters']) == 3
                assert operation['parameters'][0]['name'] == 'id'
                assert operation['parameters'][0]['in'] == 'path'
                assert operation['parameters'][0]['required'] == True
                assert operation['parameters'][1]['name'] == 'version'
                assert operation['parameters'][1]['in'] == 'path'
                assert operation['parameters'][1]['required'] == True
                assert operation['parameters'][2]['name'] == 'hash'
                assert operation['parameters'][2]['in'] == 'path'
                assert operation['parameters'][2]['required'] == True

        def describe_schema():

            def should_have_security_definition():
                to_test.swagger_app.parse_apis_info(resp)
                assert to_test.swagger_app.swagger['securityDefinitions']['HTTP Basic'] == {'type': 'basic'}
            
            def should_extract_definitions_from_response():
                endpoint = results['/space/{spaceKey}/property']
                operation = endpoint['post']
                assert 'definitions' not in operation['responses']["200"]['schema']
                assert to_test.swagger_app.definitions
                assert 'html-string' in to_test.swagger_app.definitions
                assert 'person' in to_test.swagger_app.definitions
                assert 'content-representation' in to_test.swagger_app.definitions
                assert 'unknown-user' in to_test.swagger_app.definitions
                assert 'space' in to_test.swagger_app.definitions
                assert 'content' in to_test.swagger_app.definitions
                assert 'known-user' in to_test.swagger_app.definitions
                assert 'web-resource-dependencies' in to_test.swagger_app.definitions
                assert 'version' in to_test.swagger_app.definitions
                assert 'operation-key' in to_test.swagger_app.definitions
                assert 'user' in to_test.swagger_app.definitions
                assert 'anonymous' in to_test.swagger_app.definitions
                assert 'icon' in to_test.swagger_app.definitions

            def should_extract_definitions_from_parameters():
                endpoint = results['/space/{spaceKey}/property']
                operation = endpoint['post']
                assert 'definitions' not in operation['parameters'][0]
                assert to_test.swagger_app.definitions

            def should_remove_id():
                endpoint = results['/space/{spaceKey}/property']
                operation = endpoint['post']
                assert 'id' not in operation['responses']["200"]['schema']

            def should_remove_id_from_parameters():
                endpoint = results['/space/{spaceKey}/property']
                operation = endpoint['post']
                assert 'id' not in operation['parameters'][0]

            def should_not_contain_xscope_key():
                post_item = results['/space/_private']['post']

                assert post_item['responses']['200']['description'] == "application/json Returns a full JSON representation of a space"
                assert post_item['responses']['200']['schema']['properties']['type'] == {u'$ref': u'#/definitions/space-type'}

            def describe_fix_schema_definitions():

                def should_convert_type_to_string_for_missing_object_properties():
                    assert to_test.swagger_app.definitions['html-string']['type'] == "string"
                    assert to_test.swagger_app.definitions['person']['type'] == "string"
                    assert to_test.swagger_app.definitions['content-representation']['type'] == "string"
                    assert to_test.swagger_app.definitions['operation-key']['type'] == "string"

                def should_not_convert_type_to_string_for_existing_object_properties():
                    assert to_test.swagger_app.definitions['unknown-user']['type'] == 'object'
                    assert to_test.swagger_app.definitions['space']['type'] == 'object'
                    assert to_test.swagger_app.definitions['content']['type'] == 'object'
                    assert to_test.swagger_app.definitions['known-user']['type'] == 'object'
                    assert to_test.swagger_app.definitions['user']['type'] == 'object'
