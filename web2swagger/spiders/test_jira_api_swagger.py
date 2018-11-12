# -*- coding: utf-8 -*-
# import pytest
from scrapy_tdd import *
from scrapy.selector import Selector
import json
import pytest

from api_swagger import ApiSwagger as ApiSwaggerForJira


def response_from(file_name, encoding="latin"):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name, encoding=encoding)

def describe_jira_swagger():
    config_file = os.path.join(my_path(__file__), '..', 'config', 'jira.py')

    jira_api = ApiSwaggerForJira(config_file=config_file)
    resp = response_from("JIRA 6.1 REST API documentation.html")
    results = jira_api.parse_paths(resp)

    def describe_basics_of_extraction():
        endpoint = results['/rest/api/2/attachment/{id}']

        def it_should_have_two_operations():
            assert len(endpoint) == 2
            assert ['delete', 'get'] == sorted(endpoint.keys())

        def describe_get_operation():
            get_op = endpoint['get']

            def it_should_have_a_description():
                assert get_op['description'] == u"Returns the meta-data for an attachment, including the URI of the actual attached file."

            def it_should_have_one_parameter___the_same_as_for_delete():
                print json.dumps(endpoint, indent = 4)
                assert len(get_op['parameters']) == 1
                assert get_op['parameters'][0] == {
                    "required": True,
                    "in": "path", 
                    "type": "string", 
                    "name": "id", 
                    "description": "the id of the attachment to ddelete."
                }


            def it_should_have_two_response_codes():
                assert len(get_op['responses']) == 2
                assert ['200', '404'] == sorted(get_op['responses'].keys())

            def it_should_have_a_schema_for_the_200_response():
                print get_op['responses']['200']['schema']
                assert len(get_op['responses']['200']['schema']) == 3


        def describe_delete_operation():
            delete_op = endpoint['delete']

            def it_should_have_a_description():
                assert delete_op['description'] == "Remove an attachment from an issue."

            def it_should_have_one_parameter___the_same_as_for_get():
                print json.dumps(endpoint, indent = 4)
                assert len(delete_op['parameters']) == 1
                assert delete_op['parameters'][0] == {
                    "required": True,
                    "in": "path", 
                    "type": "string", 
                    "name": "id", 
                    "description": "the id of the attachment to ddelete."
                }

            def it_should_have_three_response_codes():
                assert len(delete_op['responses']) == 3
                assert ['204', '403', '404'] == sorted(delete_op['responses'].keys())
                assert 'Returned if successful.' == delete_op['responses']['204']['description']
                assert "Returned if attachments is disabled or if you don't have permission to remove attachments from this issue." == delete_op['responses']['403']['description']
                assert 'Returned if the attachment is not found' == delete_op['responses']['404']['description']

    def describe_extraction_of_api_with_acceptable_request_body():
        endpoint = results['/rest/api/2/application-properties/{id}']
        operation = endpoint['put']
        parameter = operation['parameters'][0]
        
        def it_should_have_parameters_and_schema():
            assert len(operation['parameters']) == 2

        def it_should_have_a_description():
                assert operation['description'] == u'Modify an application property via PUT. The "value" field present in the PUT will override thee existing value.'

        def it_should_have_the_correct_parameter_data():
            assert parameter['name'] == 'id'
            assert parameter['in'] == 'path'
            assert parameter['type'] == 'string'
            assert parameter['description'] == ''

        def it_should_have_a_schema_for_the_parameter():
            assert len(operation['parameters'][1]['schema']) > 1
            assert operation['parameters'][1]['schema'] ==  {'required': [u'id', u'value'], 'type': 'object', 'properties': {u'id': {'type': 'string'}, u'value': {'type': 'string'}}}

    def describe_request_specific_parameters():
        endpoint = results['/rest/api/2/application-properties']
        operation = endpoint['get']

        def it_should_have_three_parameters():
            assert len(operation['parameters']) == 3
            assert ['key', 'permissionLevel', 'keyFilter'] == [x['name'] for x in operation['parameters']]

    def describe_parameter_types_conversion():
        endpoint = results['/rest/api/2/dashboard']
        operation = endpoint['get']

        def should_convert_int_to_integer():
            assert operation['parameters'][1]['type'] == 'integer'

        def should_convert_long_to_integer():
            endpoint = results['/rest/api/2/filter/{id}']
            operation = endpoint['get']

            assert operation['parameters'][0]['type'] == 'integer'

        def should_extract_only_boolean_value_and_no_other_strings():
            endpoint = results['/rest/api/2/search']
            operation = endpoint['get']

            assert operation['parameters'][3]['type'] == 'boolean'

    def describe_parameter():
        endpoint = results['/rest/api/2/attachment/{id}']
        operation = endpoint['get']

        def it_should_have_required_set_as_true_for_in_path():
            assert operation['parameters'][0]['required'] == True

        def it_should_have_no_required_for_in_query():
            endpoint = results['/rest/api/2/password/policy']
            operation = endpoint['get']

            assert 'required' not in operation['parameters'][0]

        def it_should_have_no_duplicate_keys():
            endpoint = results['/rest/api/2/project/{projectIdOrKey}/role/{id}']
            operation = endpoint['put']

            parameter_names_count = {}
            for x in operation['parameters']:
                if x['name'] in parameter_names_count:
                    parameter_names_count[x['name']] += 1
                else:
                    parameter_names_count[x['name']] = 1

            assert parameter_names_count['projectIdOrKey'] == 1
            assert parameter_names_count['id'] == 1

        def it_should_change_formData_to_query():
            endpoint = results['/rest/api/2/user']
            operation = endpoint['put']

            assert operation['parameters'][0]['in'] == 'query'

    def describe_regressions_and_errors():
        def should_return_parameters_schema_that_is_invalid_json():
            item = results['/rest/api/2/project/{projectIdOrKey}/role/{id}']
            assert ['delete', 'get', 'post', 'put'] == sorted(item.keys())

            post_item = item['post']
            assert post_item['parameters'][0] == {'required': True, 'in': 'path', 'type': u'string', 'name': u'projectIdOrKey', 'description': u'the project id or project key'}
            assert post_item['parameters'][1] == {'required': True, 'in': 'path', 'type': u'integer', 'name': u'id', 'description': u'the project role id'}
            assert post_item['parameters'][2] == {'schema': {'anyOf': [{'required': [u'user'], 'type': 'object', 'properties': {u'user': {'items': {'type': 'string'}, 'type': 'array'}}}, {'required': [u'group'], 'type': 'object', 'properties': {u'group': {'items': {'type': 'string'}, 'type': 'array'}}}]}, 'name': 'body', 'in': 'body'}

    def describe_schemas():
        endpoint = results['/rest/api/2/password/policy']
        operation = endpoint['get']

        def it_should_have_no_schema():
            assert 'schema' not in operation['responses']['200']

        def it_should_have_schema():
            endpoint = results['/rest/api/2/statuscategory']
            operation = endpoint['get']

            assert 'schema' in operation['responses']['200']

        def it_should_not_include_schema_that_is_not_json():
            endpoint = results['/rest/api/2/settings/baseUrl']
            operation = endpoint['put']

            assert operation['parameters'] == []

        def it_should_return_valid_schema_that_has_seperated_json():
            endpoint = results['/rest/api/2/project/{projectIdOrKey}/role/{id}']
            operation = endpoint['post']
            assert 'anyOf' in operation['parameters'][2]['schema']
            assert operation['parameters'][2]['schema']['anyOf'][0] == {'required': [u'user'], 'type': 'object', 'properties': {u'user': {'items': {'type': 'string'}, 'type': 'array'}}}
            assert operation['parameters'][2]['schema']['anyOf'][1] == {'required': [u'group'], 'type': 'object', 'properties': {u'group': {'items': {'type': 'string'}, 'type': 'array'}}}

    def describe_docs_page_1():

        def should_parse_operations_that_split_by_css_path():
            operation_html = """
                <div class="method">
                <h4 id="d2e172">GET 
                                </h4>
                <p>Returns the meta-data for an attachment, including the URI of the actual attached file.</p>
                <p><em>available response representations:</em></p>
                <ul>
                <li>
                <div>200 - application/json (<abbr title="{http://research.sun.com/wadl/2006/10} ">attachment</abbr>)
                                [<a onclick="toggle('d2e179'); return false;" href="#"><em><span id="link-d2e179">expand</span></em></a>]
                            </div>
                <div class="toggle" id="d2e179">
                <p></p>
                <h6>Example</h6>
                <pre><code>{"self":"http://www.example.com/jira/rest/api/2.0/attachments/10000","filename":"picture.jpg","author":{"self":"http://www.example.com/jira/rest/api/2/user?username=fred","name":"fred","avatarUrls":{"24x24":"http://www.example.com/jira/secure/useravatar?size=small&amp;ownerId=fred","16x16":"http://www.example.com/jira/secure/useravatar?size=xsmall&amp;ownerId=fred","32x32":"http://www.example.com/jira/secure/useravatar?size=medium&amp;ownerId=fred","48x48":"http://www.example.com/jira/secure/useravatar?size=large&amp;ownerId=fred"},"displayName":"Fred F. User","active":false},"created":"2013-08-23T16:57:35.977+0200","size":23123,"mimeType":"image/jpeg","content":"http://www.example.com/jira/attachments/10000","thumbnail":"http://www.example.com/jira/secure/thumbnail/10000"}</code></pre>
                <p>Returns a JSON representation of the attachment meta-data. The representation does not contain the
                      attachment itself, but contains a URI that can be used to download the actual attached file.</p>
                <div class="representation"></div>
                </div>
                </li>
                <li>
                <div>404<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                [<a onclick="toggle('d2e176'); return false;" href="#"><em><span id="link-d2e176">expand</span></em></a>]
                            </div>
                <div class="toggle" id="d2e176"><p>Returned if the attachment with the given id does not exist, or is not accessible by the calling user.</p></div>
                </li>
                </ul>
                </div>
                <div class="method">
                <h4 id="d2e189">DELETE 
                                </h4>
                <p>Remove an attachment from an issue.</p>
                <p><em>available response representations:</em></p>
                <ul>
                <li>
                <div>204<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                [<a onclick="toggle('d2e193'); return false;" href="#"><em><span id="link-d2e193">expand</span></em></a>]
                            </div>
                <div class="toggle" id="d2e193"><p>Returned if successful.</p></div>
                </li>
                <li>
                <div>403<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                [<a onclick="toggle('d2e199'); return false;" href="#"><em><span id="link-d2e199">expand</span></em></a>]
                            </div>
                <div class="toggle" id="d2e199"><p>Returned if attachments is disabled or if you don't have permission to remove attachments from this issue.</p></div>
                </li>
                <li>
                <div>404<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                [<a onclick="toggle('d2e196'); return false;" href="#"><em><span id="link-d2e196">expand</span></em></a>]
                            </div>
                <div class="toggle" id="d2e196"><p>Returned if the attachment is not found</p></div>
                </li>
                </ul>
                </div>
            """

            sel = Selector(text=operation_html)
            sub_selectors = jira_api.extractExtractorResults(sel, jira_api.config.get('operation'))
            assert len(sub_selectors) == 2

        def should_split_by_css_path_2():
            operation_html = """
                <div class="resource">
                    <h3 id="d2e3476">/rest/api/2/user</h3>
                    <h6>Methods</h6>
                    <div class="methods">
                    <div class="method">
                    <h4 id="d2e3477">GET 
                                    </h4>
                    <h6>/rest/api/2/user<span class="optional">?username</span><span class="optional">&amp;key</span>
                    </h6>
                    <p>Returns a user. This resource cannot be accessed anonymously.</p>
                    <h6>request query parameters</h6>
                    <table>
                    <tr>
                    <th>parameter</th>
                    <th>value</th>
                    <th>description</th>
                    </tr>
                    <tr>
                    <td><p><strong>username</strong></p></td>
                    <td><p><em><a href="http://www.w3.org/TR/xmlschema-2/#string">string</a></em></p></td>
                    <td><p>the username</p></td>
                    </tr>
                    <tr>
                    <td><p><strong>key</strong></p></td>
                    <td><p><em><a href="http://www.w3.org/TR/xmlschema-2/#string">string</a></em></p></td>
                    <td><p>user key</p></td>
                    </tr>
                    </table>
                    <p><em>available response representations:</em></p>
                    <ul>
                    <li>
                    <div>200 - application/json (<abbr title="{http://research.sun.com/wadl/2006/10} ">user</abbr>)
                                    [<a onclick="toggle('d2e3491'); return false;" href="#"><em><span id="link-d2e3491">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3491">
                    <p></p>
                    <h6>Example</h6>
                    <pre><code>{"self":"http://www.example.com/jira/rest/api/2/user?username=fred","name":"fred","emailAddress":"fred@example.com","avatarUrls":{"24x24":"http://www.example.com/jira/secure/useravatar?size=small&amp;ownerId=fred","16x16":"http://www.example.com/jira/secure/useravatar?size=xsmall&amp;ownerId=fred","32x32":"http://www.example.com/jira/secure/useravatar?size=medium&amp;ownerId=fred","48x48":"http://www.example.com/jira/secure/useravatar?size=large&amp;ownerId=fred"},"displayName":"Fred F. User","active":true,"timeZone":"Australia/Sydney","groups":{"size":3,"items":[]}}</code></pre>
                    <p>Returns a full representation of a JIRA user in JSON format.</p>
                    <div class="representation"></div>
                    </div>
                    </li>
                    <li>
                    <div>401<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3501'); return false;" href="#"><em><span id="link-d2e3501">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3501"><p>Returned if the current user is not authenticated.</p></div>
                    </li>
                    <li>
                    <div>404<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3488'); return false;" href="#"><em><span id="link-d2e3488">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3488"><p>Returned if the requested user is not found.</p></div>
                    </li>
                    </ul>
                    </div>
                    <div class="method">
                    <h4 id="d2e3504">PUT 
                                    <a href="#experimental">(experimental)</a>
                    </h4>
                    <h6>/rest/api/2/user<span class="optional">?username</span><span class="optional">&amp;key</span>
                    </h6>
                    <p>Modify user. The "value" fields present will override the existing value.
                     Fields skipped in request will not be changed.</p>
                    <h6>request query parameters</h6>
                    <table>
                    <tr>
                    <th>parameter</th>
                    <th>value</th>
                    <th>description</th>
                    </tr>
                    <tr>
                    <td><p><strong>username</strong></p></td>
                    <td><p><em><a href="http://www.w3.org/TR/xmlschema-2/#string">string</a></em></p></td>
                    <td><p>the username</p></td>
                    </tr>
                    <tr>
                    <td><p><strong>key</strong></p></td>
                    <td><p><em><a href="http://www.w3.org/TR/xmlschema-2/#string">string</a></em></p></td>
                    <td><p>user key</p></td>
                    </tr>
                    </table>
                    <p><em>acceptable request representations:</em></p>
                    <ul><li>
                    <div>application/json<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3514'); return false;" href="#"><em><span id="link-d2e3514">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3514">
                    <p></p>
                    <h6>Example</h6>
                    <pre><code>{"name":"eddie","emailAddress":"eddie@atlassian.com","displayName":"Eddie of Atlassian"}</code></pre>
                    </div>
                    </li></ul>
                    <p><em>available response representations:</em></p>
                    <ul>
                    <li>
                    <div>200 - application/json (<abbr title="{http://research.sun.com/wadl/2006/10} ">user</abbr>)
                                    [<a onclick="toggle('d2e3526'); return false;" href="#"><em><span id="link-d2e3526">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3526">
                    <p></p>
                    <h6>Example</h6>
                    <pre><code>{"self":"http://www.example.com/jirahttp://www.example.com/jira/rest/api/2/user/charlie","key":"charlie","name":"charlie","emailAddress":"charlie@atlassian.com","displayName":"Charlie of Atlassian"}</code></pre>
                    <p>Returned if the user exists and the caller has permission to edit it.</p>
                    <div class="representation"></div>
                    </div>
                    </li>
                    <li>
                    <div>400<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3536'); return false;" href="#"><em><span id="link-d2e3536">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3536"><p>Returned if the request is invalid.</p></div>
                    </li>
                    <li>
                    <div>403<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3539'); return false;" href="#"><em><span id="link-d2e3539">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3539"><p>Returned if the caller user does not have permission to edit the user.</p></div>
                    </li>
                    <li>
                    <div>404<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3523'); return false;" href="#"><em><span id="link-d2e3523">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3523"><p>Returned if the caller does have permission to edit the user but the user does not exist.</p></div>
                    </li>
                    </ul>
                    </div>
                    <div class="method">
                    <h4 id="d2e3542">POST 
                                    <a href="#experimental">(experimental)</a>
                    </h4>
                    <p>Create user. By default created user will not be notified with email.
                     If password field is not set then password will be randomly generated.</p>
                    <p><em>acceptable request representations:</em></p>
                    <ul><li>
                    <div>application/json<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3546'); return false;" href="#"><em><span id="link-d2e3546">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3546">
                    <p></p>
                    <h6>Example</h6>
                    <pre><code>{"name":"charlie","password":"abracadabra","emailAddress":"charlie@atlassian.com","displayName":"Charlie of Atlassian"}</code></pre>
                    </div>
                    </li></ul>
                    <p><em>available response representations:</em></p>
                    <ul>
                    <li>
                    <div>201<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3555'); return false;" href="#"><em><span id="link-d2e3555">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3555">
                    <p></p>
                    <h6>Example</h6>
                    <pre><code>{"self":"http://www.example.com/jirahttp://www.example.com/jira/rest/api/2/user/charlie","key":"charlie","name":"charlie","emailAddress":"charlie@atlassian.com","displayName":"Charlie of Atlassian"}</code></pre>
                    <p>Returned if the user was created.</p>
                    </div>
                    </li>
                    <li>
                    <div>400<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3565'); return false;" href="#"><em><span id="link-d2e3565">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3565"><p>Returned if the request is invalid.</p></div>
                    </li>
                    <li>
                    <div>403<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3568'); return false;" href="#"><em><span id="link-d2e3568">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3568"><p>Returned if the caller user does not have permission to create the user.</p></div>
                    </li>
                    <li>
                    <div>500<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3571'); return false;" href="#"><em><span id="link-d2e3571">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3571"><p>Returned if the user was not created because of other error.</p></div>
                    </li>
                    </ul>
                    </div>
                    <div class="method">
                    <h4 id="d2e3574">DELETE 
                                    <a href="#experimental">(experimental)</a>
                    </h4>
                    <h6>/rest/api/2/user<span class="optional">?username</span><span class="optional">&amp;key</span>
                    </h6>
                    <p>Removes user.</p>
                    <h6>request query parameters</h6>
                    <table>
                    <tr>
                    <th>parameter</th>
                    <th>value</th>
                    <th>description</th>
                    </tr>
                    <tr>
                    <td><p><strong>username</strong></p></td>
                    <td><p><em><a href="http://www.w3.org/TR/xmlschema-2/#string">string</a></em></p></td>
                    <td><p>the username</p></td>
                    </tr>
                    <tr>
                    <td><p><strong>key</strong></p></td>
                    <td><p><em><a href="http://www.w3.org/TR/xmlschema-2/#string">string</a></em></p></td>
                    <td><p>user key</p></td>
                    </tr>
                    </table>
                    <p><em>available response representations:</em></p>
                    <ul>
                    <li>
                    <div>204<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3585'); return false;" href="#"><em><span id="link-d2e3585">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3585"><p>Returned if the user was deleted successfully.</p></div>
                    </li>
                    <li>
                    <div>400<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3591'); return false;" href="#"><em><span id="link-d2e3591">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3591"><p>Returned if the request is invalid or some other server error occurred.</p></div>
                    </li>
                    <li>
                    <div>403<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3594'); return false;" href="#"><em><span id="link-d2e3594">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3594"><p>Returned if the caller does not have permission to remove the user.</p></div>
                    </li>
                    <li>
                    <div>404<abbr title="{http://research.sun.com/wadl/2006/10} "></abbr>
                                    [<a onclick="toggle('d2e3588'); return false;" href="#"><em><span id="link-d2e3588">expand</span></em></a>]
                                </div>
                    <div class="toggle" id="d2e3588"><p>Returned if the caller does have permission to remove user but the user does not exist.</p></div>
                    </li>
                    </ul>
                    </div>
                    </div>
                </div>
            """

            sel = Selector(text=operation_html)
            sub_selectors = jira_api.extractExtractorResults(sel, jira_api.config.get('operation'))
            assert len(sub_selectors) == 4

    def should_find_key_value():
        assert jira_api.is_value_exists_in_list_of_dicts(
            [{'required': True, 'in': 'path', 'type': u'string', 'name': u'projectIdOrKey', 'description': u'the project id or project key'}],
            'name', 'projectIdOrKey')

    def should_return_security_definitions():
        jira_api.parse_apis_info(resp)
        assert jira_api.swagger['securityDefinitions']['HTTP Basic'] =={'type': 'basic'}

    def describe_missing_responses():
        endpoint = results['/rest/api/2/settings/baseUrl']
        operation = endpoint['put']

        def should_have_default_response():
            assert operation['responses'] == {'200': {'description': 'Unknown'}}
