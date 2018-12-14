# -*- coding: utf-8 -*-
import pytest
import json
from scrapy_tdd import *
from scrapy.selector import Selector

from api_swagger import ApiSwagger


def response_from(file_name, encoding="latin"):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name, encoding=encoding)

def describe_jira_swagger():
    config_file = os.path.join(my_path(__file__), '..', 'config', 'dropbox_content.py')

    to_test = ApiSwagger(config_file=config_file)

    def describe_docs_page_1():
        resp = response_from('HTTP - Developers - Dropbox User Endpoints.html')
        result = to_test.parse_paths(resp)

        def should_collect_number_of_paths():
            assert len(result) == 15

        def should_contain_apis():
            assert '/paper/docs/update' in result
            assert '/sharing/get_shared_link_file' in result

        def should_not_contain_rpc_apis():
            assert 'users/get_account' not in result

        def should_update_existsing_api_with_operation():
            assert 'post' in result['/paper/docs/update']
            assert 'get' in result['/oauth2/authorize']

        def should_add_consumes_on_path_file_upload_post():
            assert result['/files/upload']['post']['consumes'] == ["application/octet-stream"]

        def should_parse_paths_with_global_attributes():
            item = result['/paper/docs/update']['post']
            assert len(item['parameters']) == 2
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

        def should_contain_description_of_operation():
            assert result['/paper/docs/update']['post']['description'] == 'Updates an existing Paper doc with the provided content.'
            assert result['/sharing/get_shared_link_file']['post']['description'] == "Download the shared link's file from a user's Dropbox."
            assert result['/files/download_zip']['post']['description'] == "Download a folder from the user's Dropbox, as a zip file. The folder must be less than 20 GB in size and have fewer than 10,000 total files. The input cannot be a single file. Any single file must be less than 4GB in size."

        def should_contain_empty_description_for_responses():
            assert result['/files/download_zip']['post']['responses']['200']['description'] == ''

        def describe_parameters():

            def should_extract_proper_type_that_is_normal():
                item = result['/oauth2/authorize']['get']
                assert item['parameters'][0]['type'] == 'string'
                assert item['parameters'][0]['name'] == 'response_type'

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
            def should_extract_proper_name():
                item = result['/files/download']['post']
                assert item['parameters'][0]['name'] == "Dropbox-API-Arg"
                assert item['parameters'][0]['in'] == "header"
                assert item['parameters'][0]['type'] == "string"

            def describe_proper_path_names():
                  def should_include_the_main_path():
                      assert '/files/download_zip' in result

        def describe_fixEndPointParameters():
            def should_add_parameter_header_for_endpoint_content_download():
                parameters = [
                    {
                        "in": "body", 
                        "type": "string", 
                        "name": "path", 
                        "description": "A unique identifier for the file."
                    }
                ]
                results = to_test.fixEndPointParameters(parameters, 'Content-download')
                assert len(results) == 1
                assert results[0]['in'] == 'header'
                assert results[0]['name'] == 'Dropbox-API-Arg'
                assert results[0]['type'] == 'string'
                assert results[0]['description'] == '{"properties": ["path"]}'

            def should_add_parameter_header_for_endpoint_content_upload():
                parameters = [
                    {
                        "in": "body", 
                        "type": "string", 
                        "name": "path", 
                        "description": "A unique identifier for the file."
                    }
                ]
                results = to_test.fixEndPointParameters(parameters, 'Content-upload')
                assert len(results) == 2
                assert results[0]['in'] == 'header'
                assert results[0]['name'] == 'Dropbox-API-Arg'
                assert results[0]['type'] == 'string'
                assert results[0]['description'] == '{"properties": ["path"]}'
                assert results[1]['in'] == 'body'
                assert results[1]['name'] == 'file'
                assert results[1]['type'] == 'file'

            def should_add_parameter_parameters_for_content_download_url():
                item = result['/sharing/get_shared_link_file']['post']
                assert len(item['parameters']) == 1

                parameter_1 = item['parameters'][0]
                assert parameter_1['name'] == "Dropbox-API-Arg"
                assert parameter_1['in'] == "header"
                assert parameter_1['type'] == "string"
                assert parameter_1['description'] == '{"properties": ["url", "path", "link_password"]}'

            def should_add_parameter_parameters_for_content_upload_url():
                item = result['/paper/docs/update']['post']
                assert len(item['parameters']) == 2

                parameter_1 = item['parameters'][0]
                assert parameter_1['name'] == "Dropbox-API-Arg"
                assert parameter_1['in'] == "header"
                assert parameter_1['type'] == "string"
                assert parameter_1['description'] == '{"properties": ["doc_id", "doc_update_policy", "revision", "import_format"]}'

                parameter_2 = item['parameters'][1]
                assert parameter_2['in'] == 'body'
                assert parameter_2['name'] == 'file'
                assert parameter_2['type'] == 'file'


