# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scrapy.utils.test import get_crawler
from scrapy_tdd import *
from scrapy.selector import Selector
import pytest
import json

from spider import ApiSwaggerSpider

import os


def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)

config_file = os.path.join(my_path(__file__), '..', 'config', 'asana.py')

def describe_swagger_spider_1():    
    to_test = ApiSwaggerSpider.from_crawler(get_crawler(), config_file=config_file)

    def describe_docs_page_1():
        resp = response_from("asana reference.html")
        results = to_test.swagger_app.parse_paths(resp)

        def should_return_swagger_paths_with_requestBody():
            item = results['/attachments/attachment-id']
            get_item = item['get']
            assert get_item['responses']['200']['schema'] == {'required': [u'data'], 'type': 'object', 'properties': {u'data': {'required': [u'created_at', u'download_url', u'host', u'id', u'name', u'parent', u'view_url'], 'type': 'object', 'properties': {u'name': {'type': 'string'}, u'parent': {'required': [u'id', u'name'], 'type': 'object', 'properties': {u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'view_url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'download_url': {'type': 'string'}, u'host': {'type': 'string'}, u'id': {'type': 'integer'}}}}}
            
            item = results['/tasks/task-id/attachments']
            get_item = item['get']
            assert get_item['responses']['200']['schema'] == {'required': [u'data'], 'type': 'object', 'properties': {u'data': {'items': {'anyOf': [{'type': 'string'}, {'required': [u'id', u'name'], 'type': 'object', 'properties': {u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}]}, 'type': 'array'}}}

        def should_return_proper_schema_json():
            response_html = """
                <code># Request
                curl -H "Authorization: Bearer &lt;personal_access_token&gt;" \
                https://app.asana.com/api/1.0/attachments/5678

                # Response
                HTTP/1.1 200
                {
                  "data": {
                    "name": "Screenshot.png",
                    "parent": {
                      "id": 1337,
                      "name": "My Task"
                    },
                    "view_url": "https://www.dropbox.com/s/1234567890abcdef/Screenshot.png",
                    "created_at": "",
                    "download_url": "https://www.dropbox.com/s/1234567890abcdef/Screenshot.png?dl=1",
                    "host": "dropbox",
                    "id": 5678
                  }
                }
                </code>
            """
            sel = Selector(text=response_html)
            print "regex: %s" % str(to_test.swagger_app.config.get('responseSchema'))
            result = to_test.swagger_app.extractJSON(sel, to_test.swagger_app.config.get('responseSchema'))
            assert result == {'required': [u'data'], 'type': 'object', 'properties': {u'data': {'required': [u'created_at', u'download_url', u'host', u'id', u'name', u'parent', u'view_url'], 'type': 'object', 'properties': {u'name': {'type': 'string'}, u'parent': {'required': [u'id', u'name'], 'type': 'object', 'properties': {u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'view_url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'download_url': {'type': 'string'}, u'host': {'type': 'string'}, u'id': {'type': 'integer'}}}}}

        def should_convert_json_schema():
            json_data = json.loads(
                """{
                  "data": {
                    "name": "Screenshot.png",
                    "parent": {
                      "id": 1337,
                      "name": "My Task"
                    },
                    "view_url": "https://www.dropbox.com/s/1234567890abcdef/Screenshot.png",
                    "created_at": "",
                    "download_url": "https://www.dropbox.com/s/1234567890abcdef/Screenshot.png?dl=1",
                    "host": "dropbox",
                    "id": 5678
                  }
                }"""
            )

            schema = to_test.swagger_app.json_to_schema(json_data)
            assert schema == {'required': [u'data'], 'type': 'object', 'properties': {u'data': {'required': [u'created_at', u'download_url', u'host', u'id', u'name', u'parent', u'view_url'], 'type': 'object', 'properties': {u'name': {'type': 'string'}, u'parent': {'required': [u'id', u'name'], 'type': 'object', 'properties': {u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'view_url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'download_url': {'type': 'string'}, u'host': {'type': 'string'}, u'id': {'type': 'integer'}}}}}

            json_data = json.loads("""
                {
                  "data": [
                    {
                      "id": 5678,
                      "name": "Background.png"
                    },
                    {
                      "id": 9012,
                      "name": "New Design Draft.pdf"
                    },
                    "~..."
                  ]
                }
            """)
            schema = to_test.swagger_app.json_to_schema(json_data)
            assert schema == {'required': [u'data'], 'type': 'object', 'properties': {u'data': {'items': {'anyOf': [{'type': 'string'}, {'required': [u'id', u'name'], 'type': 'object', 'properties': {u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}]}, 'type': 'array'}}}

            json_data = json.loads("""
                {
                  "data": {
                    "id": 5678,
                    "name": "file.txt"
                  }
                }
            """)
            schema = to_test.swagger_app.json_to_schema(json_data)
            assert schema == {'required': [u'data'], 'type': 'object', 'properties': {u'data': {'required': [u'id', u'name'], 'type': 'object', 'properties': {u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}}}

        def should_return_security_definitions():
            to_test.swagger_app.parse_apis_info(resp)
            assert to_test.swagger_app.swagger['securityDefinitions'] == {'OAuth 2': {'flow': 'accessCode', 'tokenUrl': u'https://app.asana.com/-/oauth_token', 'type': 'oauth2', 'authorizationUrl': u'https://app.asana.com/-/oauth_authorize', 'scopes': {'default': u'Provides access to all endpoints documented in our API reference. If no scopes are requested, this scope is assumed by default.', 'openid': u'Provides access to OpenID Connect ID tokens and the OpenID Connect user info endpoint.', 'profile': u'Provides access to the users name and profile photo through the OpenID Connect user info endpoint.', 'email': u'Provides access to the users email through the OpenID Connect user info endpoint.'}}}

    def describe_docs_page_2():
        resp = response_from("asana_tags.html")
        results = to_test.swagger_app.parse_paths(resp)

        def should_set_parameter_type_string_if_not_indicated():
            endpoint = results['/tags']
            operation = endpoint['post']

            assert operation['parameters'][0]['type'] == 'string'

        def should_extract_proper_path():
            assert '/workspaces/{workspace_gid}/tags' in results

        def should_not_include_example_details_on_parameter_desc():
            endpoint = results['/tags/{tag_gid}']
            operation = endpoint['get']

            assert operation['parameters'][0]['name'] == 'tag_gid'
            assert operation['parameters'][0]['description'] == 'The tag to get.'

        @pytest.mark.skip("Removed attribute from task LS-5122")
        def should_set_required_to_true_if_():
            endpoint = results['/tags/{tag_gid}']
            operation = endpoint['put']

            assert operation['parameters'][0]['required'] == True

        @pytest.mark.skip("Removed attribute from task LS-5122")
        def should_set_required_to_false_if_not_stated_on_parameter():
            endpoint = results['/tags']
            operation = endpoint['get']

            assert operation['parameters'][0]['required'] == False

        def should_contain_no_required_key_in_parameters():
            endpoint = results['/tags']
            operation = endpoint['get']
            assert 'required' not in operation['parameters'][0]

            endpoint = results['/tags/{tag_gid}']
            operation = endpoint['put']
            assert 'required' not in operation['parameters'][0]

        def should_set_in_path_for_parameters_found_in_path():
            endpoint = results['/tags/{tag_gid}']
            operation = endpoint['put']

            assert operation['parameters'][0]['name'] == 'tag_gid'
            assert operation['parameters'][0]['in'] == 'path'

    def describe_docs_page_3():
        resp = response_from("asana_projects.html")
        results = to_test.swagger_app.parse_paths(resp)

        def should_return_only_one_response_per_status():
            endpoint = results['/projects']
            operation = endpoint['post']

            assert operation['responses']['200']['description'] == ''
            assert operation['responses']['200']['schema'] == {'required': [u'data'], 'type': 'object', 'properties': {u'data': {'type': 'object'}}}

        def should_return_only_one_response_per_status_2():
            endpoint = results['/projects']
            operation = endpoint['get']

            assert operation['responses']['200']['description'] == ''
            assert operation['responses']['200']['schema'] == {'required': [u'data'], 'type': 'object', 'properties': {u'data': {'required': [u'gid', u'id', u'name', u'notes', u'null', u'resource_type'], 'type': 'object', 'properties': {u'name': {'type': 'string'}, u'notes': {'type': 'string'}, u'gid': {'type': 'string'}, u'null': {'type': 'string'}, u'id': {'type': 'integer'}, u'resource_type': {'type': 'string'}}}}}

        def should_contain_operation_description():
            assert results['/projects']['post']['description'] == 'Creates a new project in a workspace or team.'
            assert results['/projects/{project_gid}']['get']['description'] == 'Returns the complete project record for a single project.'
            assert results['/projects/{project_gid}']['put']['description'] == 'A specific, existing project can be updated by making a PUT request on the URL for that project. Only the fields provided in the data block will be updated; any unspecified fields will remain unchanged.'

        def should_add_parameters_of_main_operation_to_path_parameters_with_no_readonly_and_type_is_not_formData():
            assert len(results['/projects']['post']['parameters']) == 12
            assert  results['/projects']['post']['parameters'][0]['name'] == 'workspace'
            assert  results['/projects']['post']['parameters'][0]['in'] == 'formData'
            assert  results['/projects']['post']['parameters'][1]['name'] == 'team'
            assert  results['/projects']['post']['parameters'][1]['in'] == 'formData'
            assert  results['/projects']['post']['parameters'][2]['name'] == 'name'
            assert  results['/projects']['post']['parameters'][3]['name'] == 'owner'
            assert  results['/projects']['post']['parameters'][4]['name'] == 'due_date'
            assert  results['/projects']['post']['parameters'][5]['name'] == 'start_on'
            assert  results['/projects']['post']['parameters'][6]['name'] == 'archived'
            assert  results['/projects']['post']['parameters'][7]['name'] == 'public'
            assert  results['/projects']['post']['parameters'][8]['name'] == 'color'
            assert  results['/projects']['post']['parameters'][9]['name'] == 'notes'
            assert  results['/projects']['post']['parameters'][10]['name'] == 'html_notes'
            assert  results['/projects']['post']['parameters'][11]['name'] == 'layout'

        def should_add_post_parameters_with_put_parameters():
            to_test.swagger_app.fix_all_paths(results)
            assert len(results['/projects/{project_gid}']['put']['parameters']) == 13
            assert results['/projects/{project_gid}']['put']['parameters'][0]['name'] == 'project_gid'
            assert results['/projects/{project_gid}']['put']['parameters'][0]['in'] == 'path'
            assert results['/projects/{project_gid}']['put']['parameters'][1]['name'] == 'name'
            assert results['/projects/{project_gid}']['put']['parameters'][2]['name'] == 'owner'
            assert results['/projects/{project_gid}']['put']['parameters'][3]['name'] == 'due_date'
            assert results['/projects/{project_gid}']['put']['parameters'][4]['name'] == 'start_on'
            assert results['/projects/{project_gid}']['put']['parameters'][5]['name'] == 'archived'
            assert results['/projects/{project_gid}']['put']['parameters'][6]['name'] == 'public'
            assert results['/projects/{project_gid}']['put']['parameters'][7]['name'] == 'color'
            assert results['/projects/{project_gid}']['put']['parameters'][8]['name'] == 'notes'
            assert results['/projects/{project_gid}']['put']['parameters'][9]['name'] == 'html_notes'
            assert results['/projects/{project_gid}']['put']['parameters'][10]['name'] == 'workspace'
            assert results['/projects/{project_gid}']['put']['parameters'][11]['name'] == 'team'
            assert results['/projects/{project_gid}']['put']['parameters'][12]['name'] == 'layout'

    def describe_docs_page_4():
        resp = response_from("asana_attachments.html")
        results = to_test.swagger_app.parse_paths(resp)

        def should_collect_number_of_paths():
            assert len(results) == 2

        def should_contain_apis():
            assert '/tasks/{task_gid}/attachments' in results
            assert '/attachments/{attachment_gid}' in results

        def should_update_existsing_api_with_operation():
            assert 'get' in results['/tasks/{task_gid}/attachments']
            assert 'post' in results['/tasks/{task_gid}/attachments']

            assert 'get' in results['/attachments/{attachment_gid}']

        def should_set_proper_parameter_in_value_for_post():
            item = results['/tasks/{task_gid}/attachments']['post']
            assert item['parameters'][0]['in'] == 'path'
            assert item['parameters'][0]['name'] == 'task_gid'

            assert item['parameters'][1]['in'] == 'formData'
            assert item['parameters'][1]['name'] == 'file'

        def should_set_proper_parameter_in_value_for_get():
            item = results['/tasks/{task_gid}/attachments']['get']
            assert item['parameters'][0]['in'] == 'path'

    def describe_docs_page_5():
        resp = response_from("asana_tasks.html")
        results = to_test.swagger_app.parse_paths(resp)

        def should_contain_apis():
            assert '/tasks' in results
            assert '/tasks/{task_gid}' in results

        def should_add_post_parameters_with_put_parameters():
            to_test.swagger_app.fix_all_paths(results)

            assert len(results['/tasks/{task_gid}']['put']['parameters']) == 18
            assert results['/tasks/{task_gid}']['put']['parameters'][0]['name'] == u'task_gid'
            assert results['/tasks/{task_gid}']['put']['parameters'][0]['in'] == u'path'
            