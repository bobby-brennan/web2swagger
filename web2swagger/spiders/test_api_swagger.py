# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scrapy.utils.test import get_crawler
from scrapy_tdd import *
from scrapy.selector import Selector
import pytest

from api_swagger import ApiSwagger

import os


def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)

config_file = os.path.join(my_path(__file__), '..', 'config', 'github_back_to_back.py')

def describe_swagger_spider_1():    
    to_test = ApiSwagger(config_file=config_file)

    def describe_docs_page_1():
        resp = response_from("GitHub API v3 _ GitHub Developer Guide.html")
        results = to_test.parse_basic_info(resp)

        def should_parse_base_info_to_swagger():
            item = to_test.swagger
            assert item['basePath'] == '/'
            assert item['host'] == 'api.github.com'
            assert item['info']['title'] == 'GitHub API'
            assert item['info']['description'] == 'The GitHub API'
            assert item['info']['version'] == 'v3'

        # @pytest.mark.skip("this page is working")
        def describe_docs_page_1():
            
            # @pytest.mark.skip("this page is working in xpath and css")
            def should_parse_per_operation_to_swagger():
                operation_html = """<h2>
                    <a id="list-your-grants" class="anchor" href="#list-your-grants" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>List your grants</h2>

                    <p>You can use this API to list the set of OAuth applications that have been granted access to your account. Unlike the <a href="/v3/oauth_authorizations/#list-your-authorizations">list your authorizations</a> API, this API does not manage individual tokens. This API will return one entry for each OAuth application that has been granted access to your account, regardless of the number of tokens an application has generated for your user. The list of OAuth applications returned matches what is shown on <a href="https://github.com/settings/applications#authorized">the application authorizations settings screen within GitHub</a>. The <code>scopes</code> returned are the union of scopes authorized for the application. For example, if an application has one token with <code>repo</code> scope and another token with <code>user</code> scope, the grant will return <code>["repo", "user"]</code>.</p>

                    <pre><code>GET /applications/grants
                    </code></pre>

                    <h3>
                    <a id="response" class="anchor" href="#response" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Response</h3>

                    <pre class="highlight highlight-headers"><code>Status: 200 OK
                    Link: &lt;https://api.github.com/resource?page=2&gt;; rel="next",
                          &lt;https://api.github.com/resource?page=5&gt;; rel="last"
                    </code></pre>


                    <pre class="highlight highlight-json"><code><span class="p">[</span><span class="w">
                      </span><span class="p">{</span><span class="w">
                        </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                        </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/applications/grants/1"</span><span class="p">,</span><span class="w">
                        </span><span class="nt">"app"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                          </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"http://my-github-app.com"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"my github app"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"client_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"abcde12345fghij67890"</span><span class="w">
                        </span><span class="p">},</span><span class="w">
                        </span><span class="nt">"created_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-09-06T17:26:27Z"</span><span class="p">,</span><span class="w">
                        </span><span class="nt">"updated_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-09-06T20:39:23Z"</span><span class="p">,</span><span class="w">
                        </span><span class="nt">"scopes"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                          </span><span class="s2">"public_repo"</span><span class="w">
                        </span><span class="p">]</span><span class="w">
                      </span><span class="p">}</span><span class="w">
                    </span><span class="p">]</span><span class="w">
                    </span></code></pre>
                """
                sel = Selector(text=operation_html)
                result = to_test.parse_operation(sel)
                assert result == {u'/applications/grants': {u'get': {'responses': {u'200': {'description': u'OK', 'schema': {'items': {'required': [u'app', u'created_at', u'id', u'scopes', u'updated_at', u'url'], 'type': 'object', 'properties': {u'scopes': {'items': {'type': 'string'}, 'type': 'array'}, u'url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'updated_at': {'type': 'string'}, u'id': {'type': 'integer'}, u'app': {'required': [u'client_id', u'name', u'url'], 'type': 'object', 'properties': {u'url': {'type': 'string'}, u'name': {'type': 'string'}, u'client_id': {'type': 'string'}}}}}, 'type': 'array'}}}, 'parameters': []}}}
            
            # @pytest.mark.skip("this page is working in xpath and css")
            def should_parse_per_operation_to_swagger_2():
                operation_html = """
                    <h2>
                        <a id="create-a-new-authorization" class="anchor" href="#create-a-new-authorization" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Create a new authorization</h2>

                        <p>If you need a small number of personal access tokens, implementing the <a href="/apps/building-oauth-apps/authorizing-oauth-apps/">web flow</a> can be cumbersome. Instead, tokens can be created using the OAuth Authorizations API using <a href="/v3/auth#basic-authentication">Basic Authentication</a>. To create personal access tokens for a particular OAuth application, you must provide its client ID and secret, found on the OAuth application settings page, linked from your <a href="https://github.com/settings/developers">OAuth applications listing on GitHub</a>.</p>

                        <p>If your OAuth application intends to create multiple tokens for one user, use <code>fingerprint</code> to differentiate between them.</p>

                        <p>You can also create OAuth tokens through the web UI via the <a href="https://github.com/settings/tokens">personal access tokens settings</a>. Read more about these tokens on the <a href="https://help.github.com/articles/creating-an-access-token-for-command-line-use">GitHub Help site</a>.</p>

                        <p>Organizations that enforce SAML SSO require personal access tokens to be whitelisted. Read more about whitelisting tokens on the <a href="https://help.github.com/articles/about-identity-and-access-management-with-saml-single-sign-on">GitHub Help site</a>.</p>

                        <pre><code>POST /authorizations
                        </code></pre>

                        <h3>
                        <a id="parameters" class="anchor" href="#parameters" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Parameters</h3>

                        <table>
                        <thead>
                        <tr>
                        <th>Name</th>
                        <th>Type</th>
                        <th>Description</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                        <td><code>scopes</code></td>
                        <td><code>array</code></td>
                        <td>A list of scopes that this authorization is in.</td>
                        </tr>
                        <tr>
                        <td><code>note</code></td>
                        <td><code>string</code></td>
                        <td>
                        <strong>Required</strong>. A note to remind you what the OAuth token is for. Tokens not associated with a specific OAuth application (i.e. personal access tokens) must have a unique note.</td>
                        </tr>
                        <tr>
                        <td><code>note_url</code></td>
                        <td><code>string</code></td>
                        <td>A URL to remind you what app the OAuth token is for.</td>
                        </tr>
                        <tr>
                        <td><code>client_id</code></td>
                        <td><code>string</code></td>
                        <td>The 20 character OAuth app client key for which to create the token.</td>
                        </tr>
                        <tr>
                        <td><code>client_secret</code></td>
                        <td><code>string</code></td>
                        <td>The 40 character OAuth app client secret for which to create the token.</td>
                        </tr>
                        <tr>
                        <td><code>fingerprint</code></td>
                        <td><code>string</code></td>
                        <td>A unique string to distinguish an authorization from others created for the same client ID and user.</td>
                        </tr>
                        </tbody>
                        </table>

                        <pre class="highlight highlight-json"><code><span class="p">{</span><span class="w">
                          </span><span class="nt">"scopes"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                            </span><span class="s2">"public_repo"</span><span class="w">
                          </span><span class="p">],</span><span class="w">
                          </span><span class="nt">"note"</span><span class="p">:</span><span class="w"> </span><span class="s2">"admin script"</span><span class="w">
                        </span><span class="p">}</span><span class="w">
                        </span></code></pre>


                        <h3>
                        <a id="response-5" class="anchor" href="#response-5" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Response</h3>

                        <pre class="highlight highlight-headers"><code>Status: 201 Created
                        Location: https://api.github.com/authorizations/1
                        </code></pre>


                        <pre class="highlight highlight-json"><code><span class="p">{</span><span class="w">
                          </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/authorizations/1"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"scopes"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                            </span><span class="s2">"public_repo"</span><span class="w">
                          </span><span class="p">],</span><span class="w">
                          </span><span class="nt">"token"</span><span class="p">:</span><span class="w"> </span><span class="s2">"abcdefgh12345678"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"token_last_eight"</span><span class="p">:</span><span class="w"> </span><span class="s2">"12345678"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"hashed_token"</span><span class="p">:</span><span class="w"> </span><span class="s2">"25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"app"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                            </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"http://my-github-app.com"</span><span class="p">,</span><span class="w">
                            </span><span class="nt">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"my github app"</span><span class="p">,</span><span class="w">
                            </span><span class="nt">"client_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"abcde12345fghij67890"</span><span class="w">
                          </span><span class="p">},</span><span class="w">
                          </span><span class="nt">"note"</span><span class="p">:</span><span class="w"> </span><span class="s2">"optional note"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"note_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"http://optional/note/url"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"updated_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-09-06T20:39:23Z"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"created_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-09-06T17:26:27Z"</span><span class="p">,</span><span class="w">
                          </span><span class="nt">"fingerprint"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="w">
                        </span><span class="p">}</span><span class="w">
                        </span></code></pre>
                        """

                sel_2 = Selector(text=operation_html)
                result_2 = to_test.parse_operation(sel_2)
                endpoint = result_2['/authorizations']
                operation = endpoint['post']
                assert operation['responses']['201']['schema'] == {'required': [u'app', u'created_at', u'fingerprint', u'hashed_token', u'id', u'note', u'note_url', u'scopes', u'token', u'token_last_eight', u'updated_at', u'url'], 'type': 'object', 'properties': {u'scopes': {'items': {'type': 'string'}, 'type': 'array'}, u'token_last_eight': {'type': 'string'}, u'url': {'type': 'string'}, u'app': {'required': [u'client_id', u'name', u'url'], 'type': 'object', 'properties': {u'url': {'type': 'string'}, u'name': {'type': 'string'}, u'client_id': {'type': 'string'}}}, u'updated_at': {'type': 'string'}, u'note': {'type': 'string'}, u'token': {'type': 'string'}, u'note_url': {'type': 'string'}, u'fingerprint': {'type': 'string'}, u'hashed_token': {'type': 'string'}, u'created_at': {'type': 'string'}, u'id': {'type': 'integer'}}}
                assert operation['parameters'] == [{'in': 'formData', 'type': u'string', 'name': u'scopes', 'description': u'A list of scopes that this authorization is in.'}, {'in': 'formData', 'type': u'string', 'name': u'note', 'description': u'Required . A note to remind you what the OAuth token is for. Tokens not associated with a specific OAuth application (i.e. personal access tokens) must have a unique note.'}, {'in': 'formData', 'type': u'string', 'name': u'note_url', 'description': u'A URL to remind you what app the OAuth token is for.'}, {'in': 'formData', 'type': u'string', 'name': u'client_id', 'description': u'The 20 character OAuth app client key for which to create the token.'}, {'in': 'formData', 'type': u'string', 'name': u'client_secret', 'description': u'The 40 character OAuth app client secret for which to create the token.'}, {'in': 'formData', 'type': u'string', 'name': u'fingerprint', 'description': u'A unique string to distinguish an authorization from others created for the same client ID and user.'}]

            # @pytest.mark.skip("this page is working in xpath")
            def should_parse_per_operation_to_swagger_3_many_responses():
                operation_html = """
                    <h2>
                        <a id="get-or-create-an-authorization-for-a-specific-app" class="anchor" href="#get-or-create-an-authorization-for-a-specific-app" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Get-or-create an authorization for a specific app</h2>

                    <p>This method will create a new authorization for the specified OAuth application,
                    only if an authorization for that application doesn't already exist for the
                    user. The URL includes the 20 character client ID for the OAuth app that is
                    requesting the token. It returns the user's existing authorization for the
                    application if one is present. Otherwise, it creates and returns a new one.</p>

                    <pre><code>PUT /authorizations/clients/:client_id
                    </code></pre>

                    <h3>
                    <a id="parameters-1" class="anchor" href="#parameters-1" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Parameters</h3>

                    <table>
                    <thead>
                    <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Description</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                    <td><code>client_secret</code></td>
                    <td><code>string</code></td>
                    <td>
                    <strong>Required</strong>. The 40 character OAuth app client secret associated with the client ID specified in the URL.</td>
                    </tr>
                    <tr>
                    <td><code>scopes</code></td>
                    <td><code>array</code></td>
                    <td>A list of scopes that this authorization is in.</td>
                    </tr>
                    <tr>
                    <td><code>note</code></td>
                    <td><code>string</code></td>
                    <td>A note to remind you what the OAuth token is for.</td>
                    </tr>
                    <tr>
                    <td><code>note_url</code></td>
                    <td><code>string</code></td>
                    <td>A URL to remind you what app the OAuth token is for.</td>
                    </tr>
                    <tr>
                    <td><code>fingerprint</code></td>
                    <td><code>string</code></td>
                    <td>A unique string to distinguish an authorization from others created for the same client and user. If provided, this API is functionally equivalent to <a href="/v3/oauth_authorizations/#get-or-create-an-authorization-for-a-specific-app-and-fingerprint">Get-or-create an authorization for a specific app and fingerprint</a>.</td>
                    </tr>
                    </tbody>
                    </table>

                    <pre class="highlight highlight-json"><code><span class="p">{</span><span class="w">
                      </span><span class="nt">"client_secret"</span><span class="p">:</span><span class="w"> </span><span class="s2">"abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"scopes"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                        </span><span class="s2">"public_repo"</span><span class="w">
                      </span><span class="p">],</span><span class="w">
                      </span><span class="nt">"note"</span><span class="p">:</span><span class="w"> </span><span class="s2">"admin script"</span><span class="w">
                    </span><span class="p">}</span><span class="w">
                    </span></code></pre>


                    <h3>
                    <a id="response-if-returning-a-new-token" class="anchor" href="#response-if-returning-a-new-token" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Response if returning a new token</h3>

                    <pre class="highlight highlight-headers"><code>Status: 201 Created
                    Location: https://api.github.com/authorizations/1
                    </code></pre>


                    <pre class="highlight highlight-json"><code><span class="p">{</span><span class="w">
                      </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/authorizations/1"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"scopes"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                        </span><span class="s2">"public_repo"</span><span class="w">
                      </span><span class="p">],</span><span class="w">
                      </span><span class="nt">"token"</span><span class="p">:</span><span class="w"> </span><span class="s2">"abcdefgh12345678"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"token_last_eight"</span><span class="p">:</span><span class="w"> </span><span class="s2">"12345678"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"hashed_token"</span><span class="p">:</span><span class="w"> </span><span class="s2">"25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"app"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                        </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"http://my-github-app.com"</span><span class="p">,</span><span class="w">
                        </span><span class="nt">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"my github app"</span><span class="p">,</span><span class="w">
                        </span><span class="nt">"client_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"abcde12345fghij67890"</span><span class="w">
                      </span><span class="p">},</span><span class="w">
                      </span><span class="nt">"note"</span><span class="p">:</span><span class="w"> </span><span class="s2">"optional note"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"note_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"http://optional/note/url"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"updated_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-09-06T20:39:23Z"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"created_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-09-06T17:26:27Z"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"fingerprint"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="w">
                    </span><span class="p">}</span><span class="w">
                    </span></code></pre>


                    <h3>
                    <a id="response-if-returning-an-existing-token" class="anchor" href="#response-if-returning-an-existing-token" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Response if returning an existing token</h3>

                    <pre class="highlight highlight-headers"><code>Status: 200 OK
                    Location: https://api.github.com/authorizations/1
                    </code></pre>


                    <pre class="highlight highlight-json"><code><span class="p">{</span><span class="w">
                      </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/authorizations/1"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"scopes"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                        </span><span class="s2">"public_repo"</span><span class="w">
                      </span><span class="p">],</span><span class="w">
                      </span><span class="nt">"token"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"token_last_eight"</span><span class="p">:</span><span class="w"> </span><span class="s2">"12345678"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"hashed_token"</span><span class="p">:</span><span class="w"> </span><span class="s2">"25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"app"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                        </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"http://my-github-app.com"</span><span class="p">,</span><span class="w">
                        </span><span class="nt">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"my github app"</span><span class="p">,</span><span class="w">
                        </span><span class="nt">"client_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"abcde12345fghij67890"</span><span class="w">
                      </span><span class="p">},</span><span class="w">
                      </span><span class="nt">"note"</span><span class="p">:</span><span class="w"> </span><span class="s2">"optional note"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"note_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"http://optional/note/url"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"updated_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-09-06T20:39:23Z"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"created_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-09-06T17:26:27Z"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"fingerprint"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="w">
                    </span><span class="p">}</span><span class="w">
                    </span></code></pre>
                    """

                sel_3 = Selector(text=operation_html)
                result_3 = to_test.parse_operation(sel_3)
                assert result_3 == {u'/authorizations/clients/{client_id}': {u'put': {'responses': {u'201': {'description': u'Created', 'schema': {'required': [u'app', u'created_at', u'fingerprint', u'hashed_token', u'id', u'note', u'note_url', u'scopes', u'token', u'token_last_eight', u'updated_at', u'url'], 'type': 'object', 'properties': {u'scopes': {'items': {'type': 'string'}, 'type': 'array'}, u'token_last_eight': {'type': 'string'}, u'url': {'type': 'string'}, u'app': {'required': [u'client_id', u'name', u'url'], 'type': 'object', 'properties': {u'url': {'type': 'string'}, u'name': {'type': 'string'}, u'client_id': {'type': 'string'}}}, u'updated_at': {'type': 'string'}, u'note': {'type': 'string'}, u'token': {'type': 'string'}, u'note_url': {'type': 'string'}, u'fingerprint': {'type': 'string'}, u'hashed_token': {'type': 'string'}, u'created_at': {'type': 'string'}, u'id': {'type': 'integer'}}}}, u'200': {'description': u'OK', 'schema': {'required': [u'app', u'created_at', u'fingerprint', u'hashed_token', u'id', u'note', u'note_url', u'scopes', u'token', u'token_last_eight', u'updated_at', u'url'], 'type': 'object', 'properties': {u'scopes': {'items': {'type': 'string'}, 'type': 'array'}, u'token_last_eight': {'type': 'string'}, u'url': {'type': 'string'}, u'app': {'required': [u'client_id', u'name', u'url'], 'type': 'object', 'properties': {u'url': {'type': 'string'}, u'name': {'type': 'string'}, u'client_id': {'type': 'string'}}}, u'updated_at': {'type': 'string'}, u'note': {'type': 'string'}, u'token': {'type': 'string'}, u'note_url': {'type': 'string'}, u'fingerprint': {'type': 'string'}, u'hashed_token': {'type': 'string'}, u'created_at': {'type': 'string'}, u'id': {'type': 'integer'}}}}}, 'parameters': [{'in': 'formData', 'type': 'string', 'name': u'client_secret', 'description': u'Required . The 40 character OAuth app client secret associated with the client ID specified in the URL.'}, {'in': 'formData', 'type': 'string', 'name': u'scopes', 'description': u'A list of scopes that this authorization is in.'}, {'in': 'formData', 'type': 'string', 'name': u'note', 'description': u'A note to remind you what the OAuth token is for.'}, {'in': 'formData', 'type': 'string', 'name': u'note_url', 'description': u'A URL to remind you what app the OAuth token is for.'}, {'in': 'formData', 'type': 'string', 'name': u'fingerprint', 'description': u'A unique string to distinguish an authorization from others created for the same client and user. If provided, this API is functionally equivalent to Get-or-create an authorization for a specific app and fingerprint .'}, {'description': '', 'required': True, 'type': 'string', 'name': u'client_id', 'in': 'path'}]}}}


    # @pytest.mark.skip("this page is working")
    def describe_docs_page_2():        

        def should_parse_per_operation_to_swagger():
            operation_html = """
                <h2>
                <a id="add-assignees-to-an-issue" class="anchor" href="#add-assignees-to-an-issue" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Add assignees to an issue<a href="/apps/" class="tooltip-link github-apps-marker octicon octicon-info" title="Enabled for GitHub Apps"></a>
                </h2>

                <div class="alert note">

                <p><strong>Note:</strong> You can now use emoji in label names, add descriptions to labels, and search for labels in a repository. See the <a href="/changes/2018-02-22-label-description-search-preview">blog post</a> for full details. To access these features and receive payloads with this data during the preview period, you must provide a custom <a href="/v3/media">media type</a> in the <code>Accept</code> header:</p>

                <pre><code>application/vnd.github.symmetra-preview+json
                </code></pre>

                </div>

                <div class="alert warning">

                <p><strong>Warning:</strong> The API may change without advance notice during the preview period. Preview features are not supported for production use. If you experience any issues, contact <a href="https://github.com/contact">GitHub support</a>.</p>

                </div>

                <p>Adds up to 10 assignees to an issue. Users already assigned to an issue are not replaced.</p>

                <pre><code>POST /repos/:owner/:repo/issues/:number/assignees
                </code></pre>

                <h3>
                <a id="parameters" class="anchor" href="#parameters" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Parameters</h3>

                <table>
                <thead>
                <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Description</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                <td><code>assignees</code></td>
                <td>
                <code>array</code> of <code>strings</code>
                </td>
                <td>Usernames of people to assign this issue to. <em>NOTE: Only users with push access can add assignees to an issue. Assignees are silently ignored otherwise.</em>
                </td>
                </tr>
                </tbody>
                </table>

                <h3>
                <a id="example" class="anchor" href="#example" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Example</h3>

                <p>This example adds two assignees to the existing <code>octocat</code> assignee.</p>

                <pre class="highlight highlight-json"><code><span class="p">{</span><span class="w">
                  </span><span class="nt">"assignees"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                    </span><span class="s2">"hubot"</span><span class="p">,</span><span class="w">
                    </span><span class="s2">"other_user"</span><span class="w">
                  </span><span class="p">]</span><span class="w">
                </span><span class="p">}</span><span class="w">
                </span></code></pre>


                <h3>
                <a id="response-2" class="anchor" href="#response-2" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Response</h3>

                <pre class="highlight highlight-headers"><code>Status: 201 Created
                </code></pre>


                <pre class="highlight highlight-json"><code><span class="p">{</span><span class="w">
                  </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDU6SXNzdWUx"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World/issues/1347"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"repository_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"labels_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World/issues/1347/labels{/name}"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"comments_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World/issues/1347/comments"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World/issues/1347/events"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat/Hello-World/issues/1347"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"number"</span><span class="p">:</span><span class="w"> </span><span class="mi">1347</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"state"</span><span class="p">:</span><span class="w"> </span><span class="s2">"open"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"title"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Found a bug"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"body"</span><span class="p">:</span><span class="w"> </span><span class="s2">"I'm having a problem with this."</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"user"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                    </span><span class="nt">"login"</span><span class="p">:</span><span class="w"> </span><span class="s2">"octocat"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDQ6VXNlcjE="</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"avatar_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/images/error/octocat_happy.gif"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"gravatar_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"followers_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/followers"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"following_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/following{/other_user}"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"gists_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/gists{/gist_id}"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"starred_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/starred{/owner}{/repo}"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"subscriptions_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/subscriptions"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"organizations_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/orgs"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"repos_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/repos"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/events{/privacy}"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"received_events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/received_events"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"User"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"site_admin"</span><span class="p">:</span><span class="w"> </span><span class="kc">false</span><span class="w">
                  </span><span class="p">},</span><span class="w">
                  </span><span class="nt">"labels"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                    </span><span class="p">{</span><span class="w">
                      </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">208045946</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDU6TGFiZWwyMDgwNDU5NDY="</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World/labels/bug"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"bug"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"description"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Houston, we have a problem"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"color"</span><span class="p">:</span><span class="w"> </span><span class="s2">"f29513"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"default"</span><span class="p">:</span><span class="w"> </span><span class="kc">true</span><span class="w">
                    </span><span class="p">}</span><span class="w">
                  </span><span class="p">],</span><span class="w">
                  </span><span class="nt">"assignee"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                    </span><span class="nt">"login"</span><span class="p">:</span><span class="w"> </span><span class="s2">"octocat"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDQ6VXNlcjE="</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"avatar_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/images/error/octocat_happy.gif"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"gravatar_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"followers_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/followers"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"following_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/following{/other_user}"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"gists_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/gists{/gist_id}"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"starred_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/starred{/owner}{/repo}"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"subscriptions_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/subscriptions"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"organizations_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/orgs"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"repos_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/repos"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/events{/privacy}"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"received_events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/received_events"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"User"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"site_admin"</span><span class="p">:</span><span class="w"> </span><span class="kc">false</span><span class="w">
                  </span><span class="p">},</span><span class="w">
                  </span><span class="nt">"assignees"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w">
                    </span><span class="p">{</span><span class="w">
                      </span><span class="nt">"login"</span><span class="p">:</span><span class="w"> </span><span class="s2">"octocat"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDQ6VXNlcjE="</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"avatar_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/images/error/octocat_happy.gif"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"gravatar_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"followers_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/followers"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"following_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/following{/other_user}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"gists_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/gists{/gist_id}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"starred_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/starred{/owner}{/repo}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"subscriptions_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/subscriptions"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"organizations_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/orgs"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"repos_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/repos"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/events{/privacy}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"received_events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/received_events"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"User"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"site_admin"</span><span class="p">:</span><span class="w"> </span><span class="kc">false</span><span class="w">
                    </span><span class="p">},</span><span class="w">
                    </span><span class="p">{</span><span class="w">
                      </span><span class="nt">"login"</span><span class="p">:</span><span class="w"> </span><span class="s2">"hubot"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDQ6VXNlcjE="</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"avatar_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/images/error/hubot_happy.gif"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"gravatar_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/hubot"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"followers_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/followers"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"following_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/following{/other_user}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"gists_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/gists{/gist_id}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"starred_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/starred{/owner}{/repo}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"subscriptions_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/subscriptions"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"organizations_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/orgs"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"repos_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/repos"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/events{/privacy}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"received_events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/hubot/received_events"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"User"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"site_admin"</span><span class="p">:</span><span class="w"> </span><span class="kc">true</span><span class="w">
                    </span><span class="p">},</span><span class="w">
                    </span><span class="p">{</span><span class="w">
                      </span><span class="nt">"login"</span><span class="p">:</span><span class="w"> </span><span class="s2">"other_user"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDQ6VXNlcjE="</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"avatar_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/images/error/other_user_happy.gif"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"gravatar_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/other_user"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"followers_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/followers"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"following_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/following{/other_user}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"gists_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/gists{/gist_id}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"starred_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/starred{/owner}{/repo}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"subscriptions_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/subscriptions"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"organizations_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/orgs"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"repos_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/repos"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/events{/privacy}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"received_events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/other_user/received_events"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"User"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"site_admin"</span><span class="p">:</span><span class="w"> </span><span class="kc">false</span><span class="w">
                    </span><span class="p">}</span><span class="w">
                  </span><span class="p">],</span><span class="w">
                  </span><span class="nt">"milestone"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                    </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World/milestones/1"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat/Hello-World/milestones/v1.0"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"labels_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World/milestones/1/labels"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1002604</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDk6TWlsZXN0b25lMTAwMjYwNA=="</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"number"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"state"</span><span class="p">:</span><span class="w"> </span><span class="s2">"open"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"title"</span><span class="p">:</span><span class="w"> </span><span class="s2">"v1.0"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"description"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Tracking milestone for version 1.0"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"creator"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                      </span><span class="nt">"login"</span><span class="p">:</span><span class="w"> </span><span class="s2">"octocat"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"node_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">"MDQ6VXNlcjE="</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"avatar_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/images/error/octocat_happy.gif"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"gravatar_id"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"followers_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/followers"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"following_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/following{/other_user}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"gists_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/gists{/gist_id}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"starred_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/starred{/owner}{/repo}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"subscriptions_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/subscriptions"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"organizations_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/orgs"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"repos_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/repos"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/events{/privacy}"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"received_events_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/users/octocat/received_events"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"User"</span><span class="p">,</span><span class="w">
                      </span><span class="nt">"site_admin"</span><span class="p">:</span><span class="w"> </span><span class="kc">false</span><span class="w">
                    </span><span class="p">},</span><span class="w">
                    </span><span class="nt">"open_issues"</span><span class="p">:</span><span class="w"> </span><span class="mi">4</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"closed_issues"</span><span class="p">:</span><span class="w"> </span><span class="mi">8</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"created_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-04-10T20:09:31Z"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"updated_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2014-03-03T18:58:10Z"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"closed_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2013-02-12T13:22:01Z"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"due_on"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2012-10-09T23:39:01Z"</span><span class="w">
                  </span><span class="p">},</span><span class="w">
                  </span><span class="nt">"locked"</span><span class="p">:</span><span class="w"> </span><span class="kc">true</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"active_lock_reason"</span><span class="p">:</span><span class="w"> </span><span class="s2">"too heated"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"comments"</span><span class="p">:</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"pull_request"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
                    </span><span class="nt">"url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://api.github.com/repos/octocat/Hello-World/pulls/1347"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"html_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat/Hello-World/pull/1347"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"diff_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat/Hello-World/pull/1347.diff"</span><span class="p">,</span><span class="w">
                    </span><span class="nt">"patch_url"</span><span class="p">:</span><span class="w"> </span><span class="s2">"https://github.com/octocat/Hello-World/pull/1347.patch"</span><span class="w">
                  </span><span class="p">},</span><span class="w">
                  </span><span class="nt">"closed_at"</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"created_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-04-22T13:33:48Z"</span><span class="p">,</span><span class="w">
                  </span><span class="nt">"updated_at"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2011-04-22T13:33:48Z"</span><span class="w">
                </span><span class="p">}</span><span class="w">
                </span></code></pre>
                """

            sel = Selector(text=operation_html)
            result = to_test.parse_operation(sel)
            
            assert result[u'/repos/{owner}/{repo}/issues/{number}/assignees']['post']['responses'] == {u'201': {'description': u'Created', 'schema': {'required': [u'active_lock_reason', u'assignee', u'assignees', u'body', u'closed_at', u'comments', u'comments_url', u'created_at', u'events_url', u'html_url', u'id', u'labels', u'labels_url', u'locked', u'milestone', u'node_id', u'number', u'pull_request', u'repository_url', u'state', u'title', u'updated_at', u'url', u'user'], 'type': 'object', 'properties': {u'active_lock_reason': {'type': 'string'}, u'labels': {'items': {'required': [u'color', u'default', u'description', u'id', u'name', u'node_id', u'url'], 'type': 'object', 'properties': {u'description': {'type': 'string'}, u'default': {'type': 'boolean'}, u'url': {'type': 'string'}, u'node_id': {'type': 'string'}, u'id': {'type': 'integer'}, u'color': {'type': 'string'}, u'name': {'type': 'string'}}}, 'type': 'array'}, u'number': {'type': 'integer'}, u'assignee': {'required': [u'avatar_url', u'events_url', u'followers_url', u'following_url', u'gists_url', u'gravatar_id', u'html_url', u'id', u'login', u'node_id', u'organizations_url', u'received_events_url', u'repos_url', u'site_admin', u'starred_url', u'subscriptions_url', u'type', u'url'], 'type': 'object', 'properties': {u'following_url': {'type': 'string'}, u'events_url': {'type': 'string'}, u'organizations_url': {'type': 'string'}, u'url': {'type': 'string'}, u'gists_url': {'type': 'string'}, u'html_url': {'type': 'string'}, u'subscriptions_url': {'type': 'string'}, u'avatar_url': {'type': 'string'}, u'repos_url': {'type': 'string'}, u'received_events_url': {'type': 'string'}, u'gravatar_id': {'type': 'string'}, u'starred_url': {'type': 'string'}, u'site_admin': {'type': 'boolean'}, u'login': {'type': 'string'}, u'node_id': {'type': 'string'}, u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'followers_url': {'type': 'string'}}}, u'repository_url': {'type': 'string'}, u'closed_at': {'type': 'null'}, u'id': {'type': 'integer'}, u'title': {'type': 'string'}, u'comments': {'type': 'integer'}, u'state': {'type': 'string'}, u'body': {'type': 'string'}, u'labels_url': {'type': 'string'}, u'milestone': {'required': [u'closed_at', u'closed_issues', u'created_at', u'creator', u'description', u'due_on', u'html_url', u'id', u'labels_url', u'node_id', u'number', u'open_issues', u'state', u'title', u'updated_at', u'url'], 'type': 'object', 'properties': {u'description': {'type': 'string'}, u'title': {'type': 'string'}, u'url': {'type': 'string'}, u'labels_url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'creator': {'required': [u'avatar_url', u'events_url', u'followers_url', u'following_url', u'gists_url', u'gravatar_id', u'html_url', u'id', u'login', u'node_id', u'organizations_url', u'received_events_url', u'repos_url', u'site_admin', u'starred_url', u'subscriptions_url', u'type', u'url'], 'type': 'object', 'properties': {u'following_url': {'type': 'string'}, u'events_url': {'type': 'string'}, u'organizations_url': {'type': 'string'}, u'url': {'type': 'string'}, u'gists_url': {'type': 'string'}, u'html_url': {'type': 'string'}, u'subscriptions_url': {'type': 'string'}, u'avatar_url': {'type': 'string'}, u'repos_url': {'type': 'string'}, u'received_events_url': {'type': 'string'}, u'gravatar_id': {'type': 'string'}, u'starred_url': {'type': 'string'}, u'site_admin': {'type': 'boolean'}, u'login': {'type': 'string'}, u'node_id': {'type': 'string'}, u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'followers_url': {'type': 'string'}}}, u'number': {'type': 'integer'}, u'html_url': {'type': 'string'}, u'updated_at': {'type': 'string'}, u'due_on': {'type': 'string'}, u'state': {'type': 'string'}, u'node_id': {'type': 'string'}, u'closed_issues': {'type': 'integer'}, u'open_issues': {'type': 'integer'}, u'closed_at': {'type': 'string'}, u'id': {'type': 'integer'}}}, u'events_url': {'type': 'string'}, u'comments_url': {'type': 'string'}, u'html_url': {'type': 'string'}, u'updated_at': {'type': 'string'}, u'node_id': {'type': 'string'}, u'user': {'required': [u'avatar_url', u'events_url', u'followers_url', u'following_url', u'gists_url', u'gravatar_id', u'html_url', u'id', u'login', u'node_id', u'organizations_url', u'received_events_url', u'repos_url', u'site_admin', u'starred_url', u'subscriptions_url', u'type', u'url'], 'type': 'object', 'properties': {u'following_url': {'type': 'string'}, u'events_url': {'type': 'string'}, u'organizations_url': {'type': 'string'}, u'url': {'type': 'string'}, u'gists_url': {'type': 'string'}, u'html_url': {'type': 'string'}, u'subscriptions_url': {'type': 'string'}, u'avatar_url': {'type': 'string'}, u'repos_url': {'type': 'string'}, u'received_events_url': {'type': 'string'}, u'gravatar_id': {'type': 'string'}, u'starred_url': {'type': 'string'}, u'site_admin': {'type': 'boolean'}, u'login': {'type': 'string'}, u'node_id': {'type': 'string'}, u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'followers_url': {'type': 'string'}}}, u'pull_request': {'required': [u'diff_url', u'html_url', u'patch_url', u'url'], 'type': 'object', 'properties': {u'url': {'type': 'string'}, u'diff_url': {'type': 'string'}, u'html_url': {'type': 'string'}, u'patch_url': {'type': 'string'}}}, u'locked': {'type': 'boolean'}, u'url': {'type': 'string'}, u'created_at': {'type': 'string'}, u'assignees': {'items': {'required': [u'avatar_url', u'events_url', u'followers_url', u'following_url', u'gists_url', u'gravatar_id', u'html_url', u'id', u'login', u'node_id', u'organizations_url', u'received_events_url', u'repos_url', u'site_admin', u'starred_url', u'subscriptions_url', u'type', u'url'], 'type': 'object', 'properties': {u'following_url': {'type': 'string'}, u'events_url': {'type': 'string'}, u'organizations_url': {'type': 'string'}, u'url': {'type': 'string'}, u'gists_url': {'type': 'string'}, u'html_url': {'type': 'string'}, u'subscriptions_url': {'type': 'string'}, u'avatar_url': {'type': 'string'}, u'repos_url': {'type': 'string'}, u'received_events_url': {'type': 'string'}, u'gravatar_id': {'type': 'string'}, u'starred_url': {'type': 'string'}, u'site_admin': {'type': 'boolean'}, u'login': {'type': 'string'}, u'node_id': {'type': 'string'}, u'type': {'type': 'string'}, u'id': {'type': 'integer'}, u'followers_url': {'type': 'string'}}}, 'type': 'array'}}}}}
            assert result[u'/repos/{owner}/{repo}/issues/{number}/assignees']['post']['parameters'][0] == {'in': 'formData', 'type': 'string', 'name': u'assignees', 'description': u'Usernames of people to assign this issue to. NOTE: Only users with push access can add assignees to an issue. Assignees are silently ignored otherwise.'}
            assert result[u'/repos/{owner}/{repo}/issues/{number}/assignees']['post']['parameters'][1] == {'schema': {'required': [u'assignees'], 'type': 'object', 'properties': {u'assignees': {'items': {'type': 'string'}, 'type': 'array'}}}, 'name': 'body', 'in': 'body'}
            assert result[u'/repos/{owner}/{repo}/issues/{number}/assignees']['post']['parameters'][2] == {'description': '', 'required': True, 'type': 'string', 'name': u'owner', 'in': 'path'}
            assert result[u'/repos/{owner}/{repo}/issues/{number}/assignees']['post']['parameters'][3] == {'description': '', 'required': True, 'type': 'string', 'name': u'repo', 'in': 'path'}
            assert result[u'/repos/{owner}/{repo}/issues/{number}/assignees']['post']['parameters'][4] == {'description': '', 'required': True, 'type': 'string', 'name': u'number', 'in': 'path'}