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

        def should_parse_paths_response_with_default_status():
            get_item = result['/buckets/1/chats/2/lines.json']['get']
            assert get_item['responses']['200'] == {'description': '', 'schema': {'items': {'required': [u'app_url', u'bookmark_url', u'bucket', u'content', u'created_at', u'creator', u'id', u'inherits_status', u'parent', u'status', u'title', u'type', u'updated_at', u'url'], 'type': 'object', 'properties': {u'status': {'type': 'string'}, u'app_url': {'type': 'string'}, u'parent': {'required': [u'app_url', u'id', u'title', u'type', u'url'], 'type': 'object', 'properties': {u'url': {'type': 'string'}, u'app_url': {'type': 'string'}, u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'title': {'type': 'string'}}}, u'title': {'type': 'string'}, u'url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'creator': {'required': [u'admin', u'attachable_sgid', u'avatar_url', u'bio', u'created_at', u'email_address', u'id', u'name', u'owner', u'personable_type', u'time_zone', u'title', u'updated_at'], 'type': 'object', 'properties': {u'attachable_sgid': {'type': 'string'}, u'bio': {'type': 'null'}, u'name': {'type': 'string'}, u'title': {'type': 'string'}, u'admin': {'type': 'boolean'}, u'created_at': {'type': 'string'}, u'updated_at': {'type': 'string'}, u'time_zone': {'type': 'string'}, u'avatar_url': {'type': 'string'}, u'personable_type': {'type': 'string'}, u'owner': {'type': 'boolean'}, u'email_address': {'type': 'string'}, u'id': {'type': 'integer'}}}, u'bucket': {'required': [u'id', u'name', u'type'], 'type': 'object', 'properties': {u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'updated_at': {'type': 'string'}, u'id': {'type': 'integer'}, u'content': {'type': 'string'}, u'type': {'type': 'string'}, u'inherits_status': {'type': 'boolean'}, u'bookmark_url': {'type': 'string'}}}, 'type': 'array'}}
            
        def should_strip_empty_spaces_of_json_key_and_values():
            get_item = result['/buckets/1/chats/2.json']['get']
            assert get_item['responses']['200']['schema'] == {'required': [u'app_url', u'bookmark_url', u'bucket', u'created_at', u'creator', u'id', u'inherits_status', u'lines_url', u'position', u'status', u'title', u'topic', u'type', u'updated_at', u'url'], 'type': 'object', 'properties': {u'status': {'type': 'string'}, u'app_url': {'type': 'string'}, u'title': {'type': 'string'}, u'url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'creator': {'required': [u'admin', u'attachable_sgid', u'avatar_url', u'bio', u'company', u'created_at', u'email_address', u'id', u'name', u'owner', u'personable_type', u'time_zone', u'title', u'updated_at'], 'type': 'object', 'properties': {u'attachable_sgid': {'type': 'string'}, u'bio': {'type': 'string'}, u'name': {'type': 'string'}, u'title': {'type': 'string'}, u'admin': {'type': 'boolean'}, u'created_at': {'type': 'string'}, u'updated_at': {'type': 'string'}, u'time_zone': {'type': 'string'}, u'company': {'required': [u'id', u'name'], 'type': 'object', 'properties': {u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'avatar_url': {'type': 'string'}, u'personable_type': {'type': 'string'}, u'owner': {'type': 'boolean'}, u'email_address': {'type': 'string'}, u'id': {'type': 'integer'}}}, u'bucket': {'required': [u'id', u'name', u'type'], 'type': 'object', 'properties': {u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'name': {'type': 'string'}}}, u'updated_at': {'type': 'string'}, u'lines_url': {'type': 'string'}, u'id': {'type': 'integer'}, u'topic': {'type': 'string'}, u'position': {'type': 'integer'}, u'type': {'type': 'string'}, u'inherits_status': {'type': 'boolean'}, u'bookmark_url': {'type': 'string'}}}
        
        def should_parse_requestBody_and_parameters():
            operation_html = """
            <h2><a id="user-content-create-a-document" class="anchor" aria-hidden="true" href="#create-a-document"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Create a document</h2>
            <ul>
            <li><code>POST /buckets/1/vaults/2/documents.json</code> publishes a document in the project with ID <code>1</code> and under the vault with an ID of <code>2</code>.</li>
            </ul>
            <p><strong>Required parameters</strong>: <code>title</code> as the title of the document, and <code>content</code> as the body of the document. See our <a href="https://github.com/basecamp/bc3-api/blob/master/sections/rich_text.md">Rich text guide</a> for what HTML tags are allowed.</p>
            <p><em>Optional parameters</em>: . <code>status</code>, set to <code>active</code> to publish immediately.</p>
            <p>This endpoint will return <code>201 Created</code> with the current JSON representation of the document if the creation was a success. See the <a href="#get-a-document">Get a document</a> endpoint for more info on the payload.</p>
            <h6><a id="user-content-example-json-request" class="anchor" aria-hidden="true" href="#example-json-request"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Example JSON Request</h6>
            <div class="highlight highlight-source-json"><pre>{
              <span class="pl-s"><span class="pl-pds">"</span>title<span class="pl-pds">"</span></span>: <span class="pl-s"><span class="pl-pds">"</span>New Hire Info<span class="pl-pds">"</span></span>,
              <span class="pl-s"><span class="pl-pds">"</span>content<span class="pl-pds">"</span></span>: <span class="pl-s"><span class="pl-pds">"</span>&lt;div&gt;&lt;strong&gt;Getting started&lt;/strong&gt;&lt;/div&gt;<span class="pl-pds">"</span></span>,
              <span class="pl-s"><span class="pl-pds">"</span>status<span class="pl-pds">"</span></span>: <span class="pl-s"><span class="pl-pds">"</span>active<span class="pl-pds">"</span></span>
            }</pre></div>
            <h6><a id="user-content-copy-as-curl-2" class="anchor" aria-hidden="true" href="#copy-as-curl-2"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Copy as cURL</h6>
            <div class="highlight highlight-source-shell"><pre>curl -s -H <span class="pl-s"><span class="pl-pds">"</span>Authorization: Bearer <span class="pl-smi">$ACCESS_TOKEN</span><span class="pl-pds">"</span></span> -H <span class="pl-s"><span class="pl-pds">"</span>Content-Type: application/json<span class="pl-pds">"</span></span> \
              -d <span class="pl-s"><span class="pl-pds">'</span>{"title":"New Hire Info","content":"&lt;div&gt;&lt;strong&gt;Getting started&lt;/strong&gt;&lt;/div&gt;","status":"active"}<span class="pl-pds">'</span></span> \
              https://3.basecampapi.com/<span class="pl-smi">$ACCOUNT_ID</span>/buckets/1/vaults/2/documents.json</pre></div>
             """

            sel = Selector(text=operation_html)
            result = to_test.parse_operation(sel)
            # print result
            assert result == {u'/buckets/1/vaults/2/documents.json': {u'post': {'responses': {u'201': {'description': u'Created', 'schema': {'required': [u'content', u'status', u'title'], 'type': 'object', 'properties': {u'content': {'type': 'string'}, u'status': {'type': 'string'}, u'title': {'type': 'string'}}}}}, 'parameters': [{'in': 'query', 'type': 'string', 'name': u'title', 'description': u'title as the title of the document, and'}, {'in': 'query', 'type': 'string', 'name': u'content', 'description': u'content as the body of the document. See our Rich text guide for what HTML tags are allowed.'}, {'schema': {'required': [u'content', u'status', u'title'], 'type': 'object', 'properties': {u'content': {'type': 'string'}, u'status': {'type': 'string'}, u'title': {'type': 'string'}}}, 'name': 'body', 'in': 'body'}]}}}

        def should_return_security_definitions():
            to_test.parse_apis_info(resp)
            #assert to_test.swagger['securityDefinitions']['BearerAuth'] =={'type': 'bearer','in': 'header','name': 'ACCESS_TOKEN'}
            assert to_test.swagger['securityDefinitions']['ApiKeyAuth'] =={'type': 'apiKey','in': 'header','name': 'ACCESS_TOKEN', 'description': "a bearer token, including the prefix 'Bearer', e.g. 'Bearer abcde'"}
            assert to_test.swagger['securityDefinitions']['OAuth 2'] == {'flow': 'accessCode', 'tokenUrl': 'https://launchpad.37signals.com/authorization/token', 'type': 'oauth2', 'authorizationUrl': 'https://launchpad.37signals.com/authorization/new'}

    def describe_docs_page_2():
        resp = response_from('bc3-api_documents_templates.html')
        result = to_test.parse_paths(resp)

        def should_convert_path_to_swagger_path_format():
            assert '/templates/{template_id}/project_constructions.json' in result
            assert '/templates/:template_id/project_constructions.json' not in result

        def should_have_default_response_for_unknown():
            endpoint = result['/templates/1/project_constructions/2.json']
            operation = endpoint['get']
            
            assert operation['responses'] == {'200': {'description': 'Unknown'}}

    def describe_schemas():
        resp = response_from('basecamp_todolistgroups.html')
        result = to_test.parse_paths(resp)

        endpoint = result['/buckets/1/todolists/2/groups.json']
        operation = endpoint['post']

        def it_should_return_valid_schema_that_has_seperated_json():
            assert operation['responses']['201']['description'] == 'Created'
            assert operation['responses']['201']['schema'] == {'required': [u'name'], 'type': 'object', 'properties': {u'name': {'type': 'string'}}}
            
    def describe_parameters():
        resp = response_from('bc3-api_documents_templates.html')
        result = to_test.parse_paths(resp)

        def it_should_also_contain_parameters_from_path():
            endpoint = result['/templates/{template_id}/project_constructions.json']
            operation = endpoint['post']

            print operation['parameters']

            assert len(operation['parameters']) == 2
            assert [x['name'] == 'template_id' for x in operation['parameters']]


