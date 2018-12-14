# -*- coding: utf-8 -*-
import pytest
import json
from scrapy_tdd import *
from scrapy.selector import Selector

from api_swagger import ApiSwagger


def response_from(file_name, encoding="latin"):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name, encoding=encoding)

def describe_jira_swagger():
    config_file = os.path.join(my_path(__file__), '..', 'config', 'dropbox_rpc.py')

    to_test = ApiSwagger(config_file=config_file)

    def describe_docs_page_1():
        resp = response_from('HTTP - Developers - Dropbox User Endpoints.html')
        result = to_test.parse_paths(resp)

        def should_collect_number_of_paths():
            assert len(result) == 117

        def should_contain_apis():
            assert '/users/get_account' in result
            assert '/deprecated/create_shared_link' in result
            assert '/sharing/check_job_status' in result
            assert '/paper/docs/users/add' in result
            assert '/oauth2/authorize' in result
            assert '/oauth2/token' in result

        def should_update_existsing_api_with_operation():
            assert 'post' in result['/users/get_account']
            assert 'get' in result['/oauth2/authorize']

        def describe_response_with_multiple_return_schema():

            def should_return_security_definitions():
                to_test.parse_apis_info(resp)
                oauth = to_test.swagger['securityDefinitions']["OAuth 2"]
                assert oauth["type"] == "oauth2"
                assert oauth["flow"] == "application"
                assert oauth["authorizationUrl"] == "https://www.dropbox.com/1/oauth2/authorize"
                assert oauth["tokenUrl"] == "https://api.dropbox.com/1/oauth2/token"

        def should_parse_paths_with_global_attributes():
            item = result['/contacts/delete_manual_contacts_batch']['post']
            assert item['parameters'] == [{'in': 'body', 'name': 'body', 'schema': {'type': 'object', 'properties': {u'email_addresses': {'type': 'string', 'description': u'List of manually added contacts to be deleted.'}}}}]
            assert item['responses']['400'] == {'description': 'Bad input parameter. The response body is a plaintext message with more information.'}
            assert item['responses']['401'] == {'description': u'Bad or expired token. This can happen if the access token is expired or if the access token has been revoked by Dropbox or the user. To fix this, you should re-authenticate the user. The Content-Type of the response is JSON of type AuthError Example: invalid_access_token { "error_summary": "invalid_access_token/...", "error": { ".tag": "invalid_access_token" } } Example: invalid_select_user { "error_summary": "invalid_select_user/...", "error": { ".tag": "invalid_select_user" } } Example: invalid_select_admin { "error_summary": "invalid_select_admin/...", "error": { ".tag": "invalid_select_admin" } } Example: user_suspended { "error_summary": "user_suspended/...", "error": { ".tag": "user_suspended" } } Example: expired_access_token { "error_summary": "expired_access_token/...", "error": { ".tag": "expired_access_token" } } Example: other { "error_summary": "other/...", "error": { ".tag": "other" } } AuthError (open union) Errors occurred during authentication. This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. invalid_access_token Void The access token is invalid. invalid_select_user Void The user specified in \'Dropbox-API-Select-User\' is no longer on the team. invalid_select_admin Void The user specified in \'Dropbox-API-Select-Admin\' is not a Dropbox Business team admin. user_suspended Void The user has been suspended. expired_access_token Void The access token has expired.', 'schema': {'required': [u'error', u'error_summary'], 'type': 'object', 'properties': {u'error_summary': {'type': 'string'}, u'error': {'required': [u'.tag'], 'type': 'object', 'properties': {u'.tag': {'type': 'string'}}}}}}
            assert item['responses']['403'] == {'description': u"The user or team account doesn't have access to the endpoint or feature. The Content-Type of the response is JSON of type AccessError AccessError (open union) Error occurred because the account doesn't have permission to access the resource. This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. invalid_account_type InvalidAccountTypeError Current account type cannot access the resource. InvalidAccountTypeError (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. endpoint Void Current account type doesn't have permission to access this route endpoint. feature Void Current account type doesn't have permission to access this feature. paper_access_denied PaperAccessError Current account cannot access Paper. PaperAccessError (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. paper_disabled Void Paper is disabled. not_paper_user Void The provided user has not used Paper yet."}
            assert item['responses']['409'] == {'description': u'Endpoint-specific error. Look to the JSON response body for the specifics of the error.'}
            assert item['responses']['429'] == {'description': u'Your app is making too many requests for the given user or team and is being rate limited. Your app should wait for the number of seconds specified in the "Retry-After" response header before trying again. The Content-Type of the response can be JSON or plaintext. If it is JSON, it will be type RateLimitError You can find more information in the data ingress guide . RateLimitError Error occurred because the app is being rate limited. This datatype comes from an imported namespace originally defined in the auth namespace. reason RateLimitReason The reason why the app is being rate limited. RateLimitReason (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. too_many_requests Void You are making too many requests in the past few minutes. too_many_write_operations Void There are currently too many write operations happening in the user\'s Dropbox. retry_after UInt64 The number of seconds that the app should wait before making another request. The default for this field is 1.'}
            assert item['responses']['500'] == {'description': u'An error occurred on the Dropbox servers. Check status.dropbox.com for announcements about Dropbox service issues.'}

        def should_extract_global_responses():
            resp = response_from('HTTP - Developers - Dropbox User Endpoints.html')
            result = to_test.parse_global_path_attributes(resp)

            assert result.get('parameters') == None
            assert result.get('responses')['400']['description'] == u'Bad input parameter. The response body is a plaintext message with more information.'
            assert result.get('responses')['401']['description'] == u'Bad or expired token. This can happen if the access token is expired or if the access token has been revoked by Dropbox or the user. To fix this, you should re-authenticate the user. The Content-Type of the response is JSON of type AuthError Example: invalid_access_token { "error_summary": "invalid_access_token/...", "error": { ".tag": "invalid_access_token" } } Example: invalid_select_user { "error_summary": "invalid_select_user/...", "error": { ".tag": "invalid_select_user" } } Example: invalid_select_admin { "error_summary": "invalid_select_admin/...", "error": { ".tag": "invalid_select_admin" } } Example: user_suspended { "error_summary": "user_suspended/...", "error": { ".tag": "user_suspended" } } Example: expired_access_token { "error_summary": "expired_access_token/...", "error": { ".tag": "expired_access_token" } } Example: other { "error_summary": "other/...", "error": { ".tag": "other" } } AuthError (open union) Errors occurred during authentication. This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. invalid_access_token Void The access token is invalid. invalid_select_user Void The user specified in \'Dropbox-API-Select-User\' is no longer on the team. invalid_select_admin Void The user specified in \'Dropbox-API-Select-Admin\' is not a Dropbox Business team admin. user_suspended Void The user has been suspended. expired_access_token Void The access token has expired.'
            assert result.get('responses')['401']['schema'] == {'required': [u'error', u'error_summary'], 'type': 'object', 'properties': {u'error_summary': {'type': 'string'}, u'error': {'required': [u'.tag'], 'type': 'object', 'properties': {u'.tag': {'type': 'string'}}}}}
            assert result.get('responses')['403']['description'] == u"The user or team account doesn't have access to the endpoint or feature. The Content-Type of the response is JSON of type AccessError AccessError (open union) Error occurred because the account doesn't have permission to access the resource. This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. invalid_account_type InvalidAccountTypeError Current account type cannot access the resource. InvalidAccountTypeError (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. endpoint Void Current account type doesn't have permission to access this route endpoint. feature Void Current account type doesn't have permission to access this feature. paper_access_denied PaperAccessError Current account cannot access Paper. PaperAccessError (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. paper_disabled Void Paper is disabled. not_paper_user Void The provided user has not used Paper yet."
            assert result.get('responses')['409']['description'] == u'Endpoint-specific error. Look to the JSON response body for the specifics of the error.'
            assert result.get('responses')['429']['description'] == u'Your app is making too many requests for the given user or team and is being rate limited. Your app should wait for the number of seconds specified in the "Retry-After" response header before trying again. The Content-Type of the response can be JSON or plaintext. If it is JSON, it will be type RateLimitError You can find more information in the data ingress guide . RateLimitError Error occurred because the app is being rate limited. This datatype comes from an imported namespace originally defined in the auth namespace. reason RateLimitReason The reason why the app is being rate limited. RateLimitReason (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. too_many_requests Void You are making too many requests in the past few minutes. too_many_write_operations Void There are currently too many write operations happening in the user\'s Dropbox. retry_after UInt64 The number of seconds that the app should wait before making another request. The default for this field is 1.'
            assert result.get('responses')['500']['description'] == u'An error occurred on the Dropbox servers. Check status.dropbox.com for announcements about Dropbox service issues.'
            
        def should_not_extract_response_status_with_xx():
            item = result['/contacts/delete_manual_contacts_batch']['post']
            assert '500' in item['responses']
            assert '5xx' not in item['responses']

        def should_contain_description_of_operation():
            assert result['/users/get_account']['post']['description'] == "Get information about a user's account."
            assert result['/sharing/check_job_status']['post']['description'] == "Returns the status of an asynchronous job. Apps must have full Dropbox access to use this endpoint."
            assert result['/oauth2/token']['post']['description'].startswith(u"This endpoint only applies to apps using the authorization code flow")
            assert result['/oauth2/token']['post']['description'].endswith(u"should be provided as the password.")

        def should_contain_description_of_responses_as_empty():
            assert result['/users/get_account']['post']['responses']['200']['description'] == ''
            assert result['/sharing/check_job_status']['post']['responses']['200']['description'] == ''
            assert result['/users/get_account']['post']['responses']['200']['description'] == ''

        def describe_parameters():

            def should_extract_proper_type_that_is_normal():
                item = result['/oauth2/authorize']['get']
                assert item['parameters'][0]['type'] == 'string'
                assert item['parameters'][0]['name'] == 'response_type'

            def should_extract_proper_type_that_has_parenthesis():
                item = result['/contacts/delete_manual_contacts_batch']['post']
                assert item['parameters'][0]['schema']['properties']['email_addresses']['type'] == 'string'

                item = result['/file_requests/update']['post']
                assert item['parameters'][0]['schema']['properties']['id']['type'] == 'string'

                item = result['/auth/token/from_oauth1']['post']
                assert item['parameters'][0]['schema']['properties']['oauth1_token']['type'] == 'string'

            def should_extract_proper_type_that_has_question_mark():
                item = result['/file_properties/templates/update_for_user']['post']
                assert item['parameters'][0]['schema']['properties']['name']['type'] == 'string'

            def should_convert_list_to_string():
                item = result['/sharing/share_folder']['post']
                assert item['parameters'][0]['schema']['properties']['actions']['type'] == 'string'

            def should_convert_unknown_types_to_string():
                item = result['/files/get_temporary_upload_link']['post']
                assert item['parameters'][0]['schema']['properties']['commit_info']['type'] == 'string'

            def should_convert_float_to_integer():
                item = result['/files/get_temporary_upload_link']['post']
                assert item['parameters'][0]['schema']['properties']['duration']['type'] == 'integer'

            def should_convert_uint32_to_integer():
                item = result['/files/list_folder']['post']
                assert item['parameters'][0]['schema']['properties']['limit']['type'] == 'integer'

            def should_set_proper_parameter_in_value_for_post_field():
                item = result['/files/list_folder']['post']
                assert item['parameters'][0]['in'] == 'body'

                item = result['/files/get_temporary_upload_link']['post']
                assert item['parameters'][0]['in'] == 'body'

            def should_set_proper_parameter_in_value_for_get():
                item = result['/oauth2/authorize']['get']
                print item['parameters']
                assert item['parameters'][0]['in'] == 'query'

            def should_set_proper_parameter_in_body():
                item = result['/files/delete']['post']
                # print item['parameters']
                assert item['parameters'][0]['name'] == "body"
                assert item['parameters'][0]['in'] == "body"
                assert 'required' not in item['parameters'][0]
                assert "path" in item['parameters'][0]['schema']['properties']
                assert "parent_rev" in item['parameters'][0]['schema']['properties']

            def should_count_parameters_for_oauth_apis():
                item = result['/oauth2/token']['post']
                assert len(item['parameters']) == 5
                assert 'code' in [x['name'] for x in item['parameters']]
                assert 'grant_type' in [x['name'] for x in item['parameters']]
                assert 'client_id' in [x['name'] for x in item['parameters']]
                assert 'client_secret' in [x['name'] for x in item['parameters']]
                assert 'redirect_uri' in [x['name'] for x in item['parameters']]
                
                item = result['/oauth2/authorize']['get']
                assert len(item['parameters']) == 9


        def describe_proper_parameter_names():
            resp = response_from('HTTP - Developers - Dropbox Business.html')
            result = to_test.parse_paths(resp)

            def should_extract_proper_name():
                item = result['/file_properties/templates/update_for_team']['post']

                assert item['parameters'][0]['name'] == "body"
                assert item['parameters'][0]['in'] == "body"
                assert "template_id" in item['parameters'][0]['schema']['properties']
                assert "name" in item['parameters'][0]['schema']['properties']
                assert "description" in item['parameters'][0]['schema']['properties']
                assert "add_fields" in item['parameters'][0]['schema']['properties']

            def describe_proper_path_names():
                  def should_include_the_main_path():
                      assert '/team/get_info' in result

        def describe_fixEndPointParameters():

            def should_merge_parameters_in_body_to_schema_for_endpoint_rpc():
                parameters = [
                    {
                        "in": "body", 
                        "type": "string", 
                        "name": "path", 
                        "description": "A unique identifier for the file."
                    }, 
                    {
                        "in": "body", 
                        "type": "boolean", 
                        "name": "recursive", 
                        "description": "If true, the list folder operation will be applied recursively to all subfolders and the response will contain contents of all subfolders. The default for this field is False."
                    }, 
                    {
                        "in": "body", 
                        "type": "boolean", 
                        "name": "include_media_info", 
                        "description": "If true, FileMetadata.media_info is set for photo and video. The default for this field is False."
                    }
                ]
                results = to_test.fixEndPointParameters(parameters, 'RPC')
                assert len(results) == 1
                assert results[0]['in'] == 'body'
                assert results[0]['name'] == 'body'
                assert results[0]['schema']['type'] == 'object'
                assert results[0]['schema']['properties']['path'] == {'type': 'string', 'description': "A unique identifier for the file."}
                assert results[0]['schema']['properties']['recursive'] == {'type': 'boolean', 'description': "If true, the list folder operation will be applied recursively to all subfolders and the response will contain contents of all subfolders. The default for this field is False."}
                assert results[0]['schema']['properties']['include_media_info'] == {'type': 'boolean', 'description': "If true, FileMetadata.media_info is set for photo and video. The default for this field is False."}

            def should_merge_schema_and_parameters_to_one_schema_for_endpoint_rpc():
                parameters = [
                    {
                        "in": "body", 
                        "type": "string", 
                        "name": "path", 
                        "description": "A unique identifier for the file."
                    },
                    {
                        "schema": {
                                "required": [
                                    "error", 
                                    "error_summary"
                                ], 
                                "type": "object", 
                                "properties": {
                                    "error_summary": {
                                        "type": "string"
                                    }, 
                                    "error": {
                                        "required": [
                                            ".tag"
                                        ], 
                                        "type": "object", 
                                        "properties": {
                                            ".tag": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                ]
                results = to_test.fixEndPointParameters(parameters, 'RPC')
                assert len(results) == 1
                assert results[0]['in'] == 'body'
                assert results[0]['name'] == 'body'
                assert results[0]['schema']['type'] == 'object'
                assert results[0]['schema']['properties']['error_summary'] == {"type": "string"}
                assert results[0]['schema']['properties']['error'] == {"required": [".tag"], "type": "object", "properties": {".tag": {"type": "string"}}}
                assert results[0]['schema']['properties']['path'] == {'type': 'string', 'description': "A unique identifier for the file."}

            def should_merge_required_names_for_endpoint_rpc():
                parameters = [
                    {
                        "in": "body", 
                        "type": "string", 
                        "name": "path", 
                        "description": "A unique identifier for the file.",
                        "required": True
                    }, 
                    {
                        "in": "body", 
                        "type": "boolean", 
                        "name": "recursive", 
                        "description": "If true, the list folder operation will be applied recursively to all subfolders and the response will contain contents of all subfolders. The default for this field is False.",
                        "required": False
                    }
                ]
                results = to_test.fixEndPointParameters(parameters, 'RPC')

                assert len(results) == 1
                assert results[0]['in'] == 'body'
                assert results[0]['name'] == 'body'
                assert results[0]['schema']['type'] == 'object'
                assert results[0]['schema']['required'] == ["path"]
                assert results[0]['schema']['properties']['path'] == {'type': 'string', 'description': "A unique identifier for the file."}
                assert results[0]['schema']['properties']['recursive'] == {'type': 'boolean', 'description': "If true, the list folder operation will be applied recursively to all subfolders and the response will contain contents of all subfolders. The default for this field is False."}
        
            def should_merge_schema_required_names_for_endpoint_rpc():
                parameters = [
                    {
                        "in": "body", 
                        "type": "string", 
                        "name": "path", 
                        "description": "A unique identifier for the file.",
                        "required": True
                    },
                    {
                        "schema": {
                                "required": [
                                    "error", 
                                    "error_summary"
                                ], 
                                "type": "object", 
                                "properties": {
                                    "error_summary": {
                                        "type": "string"
                                    }, 
                                    "error": {
                                        "required": [
                                            ".tag"
                                        ], 
                                        "type": "object", 
                                        "properties": {
                                            ".tag": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                ]
                results = to_test.fixEndPointParameters(parameters, 'RPC')
                assert len(results) == 1
                assert results[0]['in'] == 'body'
                assert results[0]['name'] == 'body'
                assert results[0]['schema']['type'] == 'object'
                assert results[0]['schema']['required'] == ["error", "error_summary", "path"]
                assert results[0]['schema']['properties']['error_summary'] == {"type": "string"}
                assert results[0]['schema']['properties']['error'] == {"required": [".tag"], "type": "object", "properties": {".tag": {"type": "string"}}}
                assert results[0]['schema']['properties']['path'] == {'type': 'string', 'description': "A unique identifier for the file."}

