# -*- coding: utf-8 -*-
import pytest
from scrapy_tdd import *
from scrapy.selector import Selector

from api_swagger import ApiSwagger


def response_from(file_name, encoding="latin"):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name, encoding=encoding)

def describe_jira_swagger():
    config_file = os.path.join(my_path(__file__), '..', 'config', 'dropbox.py')

    to_test = ApiSwagger(config_file=config_file)

    def describe_docs_page_1():
        resp = response_from('HTTP - Developers - Dropbox User Endpoints.html')
        result = to_test.parse_paths(resp)

        def describe_response_with_multiple_return_schema():
            operation_html = """
            <div class="documentation"><h1>Dropbox API v2</h1>
                <p>The Dropbox API allows developers to work with files in Dropbox, including advanced functionality like full-text search, thumbnails, and sharing. The <a href="https://dropbox.github.io/dropbox-api-v2-explorer/">Dropbox API explorer</a> is the easiest way to get started making API calls.
                </p><h2 id="formats">Request and response formats</h2>
                <p>In general, the Dropbox API uses HTTP POST requests with JSON arguments and JSON responses. Request authentication is via OAuth 2.0 using the <code>Authorization</code> request header or <code>authorization</code> URL parameter.
                </p>
                <p>The <code>.tag</code> field in an object identifies the subtype of a struct or selected member of a union.
                </p>
                <p>When specifying a <code>Void</code> member of a union, you may supply just the member string in place of the entire tagged union object. For example, when supplying a <code>WriteMode</code>, you can supply just <code>"mode": "add"</code> instead of <code>"mode": {".tag": "add"}}</code>. This shorthand is not allowed for non-<code>Void</code> members. For example, the following is not allowed for a <code>WriteMode</code>, as <code>update</code> is not a <code>Void</code> member: <code>"mode": "update"</code>.
                </p><h4 id="rpc-endpoints">RPC endpoints</h4>
                <p>These endpoints accept arguments as JSON in the request body and return results as JSON in the response body. RPC endpoints are on the <code>api.dropboxapi.com</code> domain.
                </p><h4 id="content-upload-endpoints">Content-upload endpoints</h4>
                <p>These endpoints accept file content in the request body, so their arguments are instead passed as JSON in the <code>Dropbox-API-Arg</code> request header or <code>arg</code> URL parameter. These endpoints are on the <code>content.dropboxapi.com</code> domain.
                </p><h4 id="content-download-endpoints">Content-download endpoints</h4>
                <p>As with content-upload endpoints, arguments are passed in the <code>Dropbox-API-Arg</code> request header or <code>arg</code> URL parameter. The response body contains file content, so the result will appear as JSON in the <code>Dropbox-API-Result</code> response header. These endpoints are also on the <code>content.dropboxapi.com</code> domain.
                </p>
                <p>These endpoints also support HTTP GET along with <code>ETag</code>-based caching (<code>If-None-Match</code>) and HTTP range requests.
                </p>
                <p>For information on how to properly encode the JSON, see the <a href="/developers/reference/json-encoding">JSON encoding page</a>.
                </p><h4 id="cors">Browser-based JavaScript and CORS pre-flight requests</h4>
                <p>When browser-based JavaScript code makes a cross-site HTTP request, the browser must sometimes send a "pre-flight" check to make sure the server allows cross-site requests. You can avoid the extra round-trip by ensuring your request meets the CORS definition of a "simple cross-site request".
                </p>
                <ul><li>Use URL parameters <code>arg</code> and <code>authorization</code> instead of HTTP headers <code>Dropbox-API-Arg</code> and <code>Authorization</code>.</li><li>Set the <code>Content-Type</code> to "text/plain; charset=dropbox-cors-hack" instead of "application/json" or "application/octet-stream".</li><li>Always set the URL parameter <code>reject_cors_preflight=true</code>. This makes it easier to catch cases where your code is unintentionally triggering a pre-flight check.</li>
                </ul><h4 id="date-format">Date format</h4>
                <p>All dates in the API use UTC and are strings in the <a href="https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations">ISO 8601 "combined date and time representation" format</a>:
                </p>
                <p><code>2015-05-15T15:50:38Z</code>
                </p><h4 id="path-formats">Path formats</h4>
                <p>Paths are relative to an application's root (either an app folder or the root of a user's Dropbox, depending on the app's <a href="/developers/reference/developer-guide#app-permissions">access type</a>). The empty string (<code>""</code>) represents the root folder. All other paths must start with a slash (e.g. <code>"/hello/world.txt"</code>). Paths may not end with a slash or whitespace. For other path restrictions, refer to <a href="https://www.dropbox.com/help/syncing-uploads/files-not-syncing">the help center</a>.
                </p>
                <p>Every file and folder in Dropbox also has an ID (e.g. <code>"id:abc123xyz"</code>) that can be obtained from any endpoint that returns metadata. Some endpoints, as noted in the individual endpoint documentation below, can accept IDs in addition to normal paths. A path relative to a folder's ID can be constructed by using a slash (e.g. <code>"id:abc123xyz/hello.txt"</code>).
                </p>
                <p>For endpoints that accept performing actions on behalf of a team administrator using the <a href="/developers/documentation/http/teams#teams-member-file-access"><code>Dropbox-API-Select-Admin header</code></a>, files may be referenced using a namespace-relative path (e.g. <code>"ns:123456/cupcake.png"</code>). In this case, the namespace ID, <code>"123456"</code>, would be the <code>shared_folder_id</code> or <code>team_folder_id</code> of the shared folder or the team folder containing the file or folder, and the path, <code>"/cupcake.png"</code>, would be the logical path to the content relative to its shared folder or team folder container.
                </p><h4 id="case-insensitivity">Case insensitivity</h4>
                <p>Like Dropbox itself, the Dropbox API is case-insensitive, meaning that /A/B/c.txt is the same file as /a/b/C.txt and is the same file as /a/B/c.txt.
                </p>
                <p>This can cause problems for apps that store file metadata from users in case-sensitive databases (such as SQLite or Postgres). Case insensitive collations should be used when storing Dropbox metadata in such databases. Alternatively, developers need to make sure their query operators are explicitly case insensitive.
                </p>
                <p>Also, while Dropbox is case-insensitive, it makes efforts to be case-preserving. <code>Metadata.name</code> will contain the correct case. <code>Metadata.path_display</code> usually will contain the correct case, but sometimes only in the last path component. If your app needs the correct case for all components, it can get it from the <code>Metadata.name</code> or last path component of each relevant <code>Metadata.path_display</code> entry.
                </p><h2 id="authorization">Authorization</h2>
                <p>Dropbox supports <a href="http://oauth.net">OAuth 2.0</a> for authorizing API requests. Find out more in our <a href="/developers/reference/oauthguide">OAuth guide</a>. Authorized requests to the API should use an <code>Authorization</code> header with the value <code>Bearer &lt;TOKEN&gt;</code>, where <code>&lt;TOKEN&gt;</code> is an access token obtained through the OAuth flow.
                </p>
                <p><strong>Note:</strong> OAuth is an authorization protocol, not an authentication protocol. Dropbox should not be used as an identity provider.
                </p><h3 id="oauth2-authorize" class="method-title">/oauth2/authorize</h3><dl><dt>Description</dt>
                <dd>
                <p>This starts the OAuth 2.0 authorization flow. This isn't an API call&mdash;it's the web page that lets the user sign in to Dropbox and authorize your app. After the user decides whether or not to authorize your app, they will be redirected to the URI specified by <code>redirect_uri</code>.
                </p>
                <p>OAuth 2.0 supports two authorization flows:
                </p>
                <ul><li>The <code>code</code> flow returns a code via the <code>redirect_uri</code> callback which should then be converted into a bearer token using the <a href="#oa2-token"><code>/oauth2/token</code> call</a>. This is the recommended flow for apps that are running on a server.</li><li>The <code>token</code> or implicit grant flow returns the bearer token via the <code>redirect_uri</code> callback, rather than requiring your app to make a second call to a server. This is useful for pure client-side apps, such as mobile apps or JavaScript-based apps.</li>
                </ul>
                <p> For more information on the two flows, see <a href="http://tools.ietf.org/html/rfc6749#section-1.3">Section 1.3 of the OAuth 2 spec</a>.
                </p>
                <p>If the user isn't already signed in to the Dropbox web site, they will be prompted to do so on this web page. Note that some users use their Google account to sign in to Dropbox. In order to comply with <a href="https://developers.googleblog.com/2016/08/modernizing-oauth-interactions-in-native-apps.html">Google's policy against processing the OAuth flow inside a web-view</a>, you should not display this web page inside a web-view.
                </p>
                </dd><dt class="url-label">URL Structure</dt>
                <dd><pre class="literal-block"><strong>https://www.dropbox.com</strong>/oauth2/authorize</pre>
                <p><strong>Note:</strong> This is the only step that requires an endpoint on <code>www.dropbox.com</code>. All other API requests are done via <code>api.dropboxapi.com</code>, <code>content.dropboxapi.com</code>, or <code>notify.dropboxapi.com</code>.
                </p>
                </dd><dt>Method</dt>
                <dd>GET
                </dd><dt>Parameters</dt>
                <dd><div class="field"><b><code>response_type</code></b> <i class="type show_datatype">String</i> The grant type requested, either <code>token</code> or <code>code</code>.
                </div><div class="field"><b><code>client_id</code></b> <i class="type show_datatype">String</i> The app's key, found in the <a href="/developers/apps">App Console</a>.
                </div><div class="field"><b><code>redirect_uri</code></b> <i class="type show_datatype">String?</i> Where to redirect the user after authorization has completed. This must be the exact URI registered in the <a href="/developers/apps">App Console</a>; even 'localhost' must be listed if it is used for testing. All redirect URIs must be HTTPS except for localhost URIs. A redirect URI is required for the <code>token</code> flow, but optional for the <code>code</code> flow. If the redirect URI is omitted, the <code>code</code> will be presented directly to the user and they will be invited to enter the information in your app.
                </div><div class="field"><b><code>state</code></b> <i class="type show_datatype">String?</i> Up to 500 bytes of arbitrary data that will be passed back to your redirect URI. This parameter should be used to protect against cross-site request forgery (CSRF). See Sections <a href="http://tools.ietf.org/html/rfc6819#section-4.4.1.8">4.4.1.8</a> and <a href="http://tools.ietf.org/html/rfc6819#section-4.4.2.5">4.4.2.5</a> of the OAuth 2.0 threat model spec.
                </div><div class="field"><b><code>require_role</code></b> <i class="type show_datatype">String?</i> If this parameter is specified, the user will be asked to authorize with a particular type of Dropbox account, either <code>work</code> for a team account or <code>personal</code> for a personal account. Your app should still verify the type of Dropbox account after authorization since the user could modify or remove the <code>require_role</code> parameter.
                </div><div class="field"><b><code>force_reapprove</code></b> <i class="type show_datatype">Boolean?</i> Whether or not to force the user to approve the app again if they've already done so. If <code>false</code> (default), a user who has already approved the application may be automatically redirected to the URI specified by <code>redirect_uri</code>. If <code>true</code>, the user will not be automatically redirected and will have to approve the app again.
                </div><div class="field"><b><code>disable_signup</code></b> <i class="type show_datatype">Boolean?</i> When true (default is false) users will not be able to sign up for a Dropbox account via the authorization page. Instead, the authorization page will show a link to the Dropbox iOS app in the App Store. This is only intended for use when necessary for compliance with App Store policies.
                </div><div class="field"><b><code>locale</code></b> <i class="type show_datatype">String?</i> If the locale specified is a <a href="/help/31">supported language</a>, Dropbox will direct users to a translated version of the authorization website. Locale tags should be <a href="http://en.wikipedia.org/wiki/IETF_language_tag">IETF language tags</a>.
                </div><div class="field"><b><code>force_reauthentication</code></b> <i class="type show_datatype">Boolean?</i> When <code>true</code> (default is <code>false</code>) users will be signed out if they are currently signed in. This will make sure the user is brought to a page where they can create a new account or sign in to another account. This should only be used when there is a definite reason to believe that the user needs to sign in to a new or different account.
                </div>
                </dd><dt>Returns</dt>
                <dd>
                <p>Because <code>/oauth2/authorize</code> is a website, there is no direct return value. However, after the user authorizes your app, they will be sent to your redirect URI. The type of response varies based on the <code>response_type</code>.
                </p><h4>Code flow</h4>
                <p>These parameters are passed in the query string (after the ? in the URL):
                </p><div class="field"><code>code</code> <i class="type show_datatype">String</i> The authorization code, which can be used to attain a bearer token by calling <a href="#oa2-token"><code>/oauth2/token</code></a>.
                </div><div class="field"><code>state</code> <i class="type show_datatype">String</i> The state content, if any, originally passed to <code>/oauth2/authorize</code>.
                </div>
                <p><strong>Sample response</strong>
                </p><pre class="literal-block">[REDIRECT_URI]?code=ABCDEFG&amp;state=[STATE]</pre><h4>Token flow</h4>
                <p>These parameters are passed in the URL fragment (after the # in the URL).
                </p>
                <p><strong>Note:</strong> as fragments, these parameters can be modified by the user and must not be trusted server-side. If any of these fields are being used server-side, please consider using the <strong>Code flow</strong>, or alternatively using the fields returned from <a href="#users-get_current_account"><code>/get_current_account</code></a> instead.
                </p><div class="field"><code>access_token</code> <i class="type show_datatype">String</i> A token which can be used to make calls to the Dropbox API.
                </div><div class="field"><code>token_type</code> <i class="type show_datatype">String</i> The type of token, which will always be <code>bearer</code>.
                </div><div class="field"><code>account_id</code> <i class="type show_datatype">String</i> A user's account identifier used by API v2.
                </div><div class="field"><code>team_id</code> <i class="type show_datatype">String</i> A team's identifier used by API v2.
                </div><div class="field"><code>uid</code> <i class="type show_datatype">String</i> Deprecated. The API v1 user/team identifier. Please use <code>account_id</code> instead, or if using the Dropbox Business API, <code>team_id</code>.
                </div><div class="field"><code>state</code> <i class="type show_datatype">String</i> The state content, if any, originally passed to <code>/oauth2/authorize</code>.
                </div>
                <p><strong>Sample response</strong>
                </p><pre class="literal-block">[REDIRECT_URI]#access_token=ABCDEFG&amp;token_type=bearer&amp;account_id=dbid%3AAAH4f99T0taONIb-OurWxbNQ6ywGRopQngc&amp;uid=12345&amp;state=[STATE]</pre>
                </dd><dt>Errors</dt>
                <dd>
                <p>In either flow, if an error occurs, including if the user has chosen not to authorize the app, the following parameters will be included in the redirect URI:
                </p><div class="field"><code>error</code> <i class="type show_datatype">String</i> An error code per <a href="http://tools.ietf.org/html/rfc6749#section-4.1.2.1">Section 4.1.2.1 of the OAuth 2.0 spec</a>.
                </div><div class="field"><code>error_description</code> <i class="type show_datatype">String</i> A user-friendly description of the error that occurred.
                </div><div class="field"><code>state</code> <i class="type show_datatype">String</i> The state content, if any, originally passed to <code>/oauth2/authorize</code>.
                </div>
                </dd></dl><h3 id="oauth2-token" class="method-title">/oauth2/token</h3><dl><dt>Description</dt>
                <dd>
                <p>This endpoint only applies to apps using the <a href="#oa2-authorize">authorization code flow</a>. An app calls this endpoint to acquire a bearer token once the user has authorized the app.
                </p>
                <p>Calls to <code>/oauth2/token</code> need to be authenticated using the apps's key and secret. These can either be passed as <code>application/x-www-form-urlencoded</code> POST parameters (see parameters below) or via <a href="https://en.wikipedia.org/wiki/Basic_access_authentication">HTTP basic authentication</a>. If basic authentication is used, the app key should be provided as the username, and the app secret should be provided as the password.
                </p>
                </dd><dt class="url-label">URL Structure</dt>
                <dd><pre class="literal-block">https://api.dropboxapi.com/oauth2/token</pre>
                </dd><dt>Method</dt>
                <dd>POST
                </dd><dt>Parameters</dt>
                <dd><div class="field"><code>code</code> <i class="type show_datatype">String</i> The code acquired by directing users to <code>/oauth2/authorize?response_type=code</code>.
                </div><div class="field"><code>grant_type</code> <i class="type show_datatype">String</i> The grant type, which must be <code>authorization_code</code>.
                </div><div class="field"><code>client_id</code> <i class="type show_datatype">String?</i> If credentials are passed in <code>POST</code> parameters, this parameter should be present and should be the app's key (found in the <a href="/developers/apps">App Console</a>).
                </div><div class="field"><code>client_secret</code> <i class="type show_datatype">String?</i> If credentials are passed in <code>POST</code> parameters, this parameter should be present and should be the app's secret.
                </div><div class="field"><code>redirect_uri</code> <i class="type show_datatype">String?</i> Only used to validate that it matches the original <code>/oauth2/authorize</code>, not used to redirect again.
                </div>
                </dd><dt>Returns</dt>
                <dd>
                <p>A JSON-encoded dictionary including an access token (<code>access_token</code>), token type (<code>token_type</code>), an API v2 user ID (<code>account_id</code>), or if team-linked, an API v2 team ID (<code>team_id</code>) instead. The API v1 identifier value (<code>uid</code>) is deprecated and should no longer be used. The token type will always be "bearer".
                </p>
                <p><strong>Sample response</strong>
                </p><pre class="literal-block">{"access_token": "ABCDEFG", "token_type": "bearer", "account_id": "dbid:AAH4f99T0taONIb-OurWxbNQ6ywGRopQngc", "uid": "12345"}</pre>
                </dd></dl><div id="error-handling" class="section toc-el"><h2>Errors</h2>
                <p>Errors are returned using standard HTTP error code syntax. Depending on the status code, the response body may be in JSON or plaintext.
                </p><h2>Errors by status code</h2><table class="api-param-values center-first-col"><tr><th>Code</th><th>Description</th></tr><tr><td>400</td><td>Bad input parameter. The response body is a plaintext message with more information.</td></tr><tr><td>401</td><td>Bad or expired token. This can happen if the access token is expired or if the access token has been revoked by Dropbox or the user. To fix this, you should re-authenticate the user. <div class="field">The  Content-Type of the response is JSON of type<i class="type show_datatype"><a>AuthError</a></i><div class="nested-child collapse">
                <div>
                <div>Example: invalid_access_token
                </div><pre class="last literal-block">{
                    &quot;error_summary&quot;: &quot;invalid_access_token/...&quot;,
                    &quot;error&quot;: {
                        &quot;.tag&quot;: &quot;invalid_access_token&quot;
                    }
                }</pre>
                <div>Example: invalid_select_user
                </div><pre class="last literal-block">{
                    &quot;error_summary&quot;: &quot;invalid_select_user/...&quot;,
                    &quot;error&quot;: {
                        &quot;.tag&quot;: &quot;invalid_select_user&quot;
                    }
                }</pre>
                <div>Example: invalid_select_admin
                </div><pre class="last literal-block">{
                    &quot;error_summary&quot;: &quot;invalid_select_admin/...&quot;,
                    &quot;error&quot;: {
                        &quot;.tag&quot;: &quot;invalid_select_admin&quot;
                    }
                }</pre>
                <div>Example: user_suspended
                </div><pre class="last literal-block">{
                    &quot;error_summary&quot;: &quot;user_suspended/...&quot;,
                    &quot;error&quot;: {
                        &quot;.tag&quot;: &quot;user_suspended&quot;
                    }
                }</pre>
                <div>Example: expired_access_token
                </div><pre class="last literal-block">{
                    &quot;error_summary&quot;: &quot;expired_access_token/...&quot;,
                    &quot;error&quot;: {
                        &quot;.tag&quot;: &quot;expired_access_token&quot;
                    }
                }</pre>
                <div>Example: other
                </div><pre class="last literal-block">{
                    &quot;error_summary&quot;: &quot;other/...&quot;,
                    &quot;error&quot;: {
                        &quot;.tag&quot;: &quot;other&quot;
                    }
                }</pre><div id="AuthError"><div class="title">AuthError <i>(open union)</i>
                </div>Errors occurred during authentication. This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves.<div class="field"><b><code>invalid_access_token</code></b> <i class="type show_datatype">Void</i> The access token is invalid.
                </div><div class="field"><b><code>invalid_select_user</code></b> <i class="type show_datatype">Void</i> The user specified in 'Dropbox-API-Select-User' is no longer on the team.
                </div><div class="field"><b><code>invalid_select_admin</code></b> <i class="type show_datatype">Void</i> The user specified in 'Dropbox-API-Select-Admin' is not a Dropbox Business team admin.
                </div><div class="field"><b><code>user_suspended</code></b> <i class="type show_datatype">Void</i> The user has been suspended.
                </div><div class="field"><b><code>expired_access_token</code></b> <i class="type show_datatype">Void</i> The access token has expired.
                </div>
                </div>
                </div>
                </div>
                </div></td></tr><tr><td>403</td><td>The user or team account doesn't have access to the endpoint or feature. <div class="field">The  Content-Type of the response is JSON of type<i class="type show_datatype"><a>AccessError</a></i><div class="nested-child collapse">
                <div><div id="AccessError"><div class="title">AccessError <i>(open union)</i>
                </div>Error occurred because the account doesn't have permission to access the resource. This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves.<div class="field"><b><code>invalid_account_type</code></b> <i class="type show_datatype"><a>InvalidAccountTypeError</a></i> Current account type cannot access the resource.<div class="nested-child collapse">
                <div><div id="InvalidAccountTypeError"><div class="title">InvalidAccountTypeError <i>(open union)</i>
                </div> This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves.<div class="field"><b><code>endpoint</code></b> <i class="type show_datatype">Void</i> Current account type doesn't have permission to access this route endpoint.
                </div><div class="field"><b><code>feature</code></b> <i class="type show_datatype">Void</i> Current account type doesn't have permission to access this feature.
                </div>
                </div>
                </div>
                </div>
                </div><div class="field"><b><code>paper_access_denied</code></b> <i class="type show_datatype"><a>PaperAccessError</a></i> Current account cannot access Paper.<div class="nested-child collapse">
                <div><div id="PaperAccessError"><div class="title">PaperAccessError <i>(open union)</i>
                </div> This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves.<div class="field"><b><code>paper_disabled</code></b> <i class="type show_datatype">Void</i> Paper is disabled.
                </div><div class="field"><b><code>not_paper_user</code></b> <i class="type show_datatype">Void</i> The provided user has not used Paper yet.
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div></td></tr><tr><td>409</td><td>Endpoint-specific error. Look to the JSON response body for the specifics of the error.</td></tr><tr><td>429</td><td>Your app is making too many requests for the given user or team and is being rate limited. Your app should wait for the number of seconds specified in the "Retry-After" response header before trying again. <div class="field">The Content-Type of the response can be JSON or plaintext. If it is JSON, it will be type<i class="type show_datatype"><a>RateLimitError</a></i>You can find more information in the <a href="/developers/reference/data-ingress-guide">data ingress guide</a>.<div class="nested-child collapse">
                <div><div id="RateLimitError"><div class="title">RateLimitError
                </div>Error occurred because the app is being rate limited. This datatype comes from an imported namespace originally defined in the auth namespace.<div class="field"><b><code>reason</code></b> <i class="type show_datatype"><a>RateLimitReason</a></i> The reason why the app is being rate limited.<div class="nested-child collapse">
                <div><div id="RateLimitReason"><div class="title">RateLimitReason <i>(open union)</i>
                </div> This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves.<div class="field"><b><code>too_many_requests</code></b> <i class="type show_datatype">Void</i> You are making too many requests in the past few minutes.
                </div><div class="field"><b><code>too_many_write_operations</code></b> <i class="type show_datatype">Void</i> There are currently too many write operations happening in the user's Dropbox.
                </div>
                </div>
                </div>
                </div>
                </div><div class="field"><b><code>retry_after</code></b> <i class="type show_datatype">UInt64</i> The number of seconds that the app should wait before making another request. The default for this field is 1.
                </div>
                </div>
                </div>
                </div>
                </div></td></tr><tr><td>500</td><td>An error occurred on the Dropbox servers. Check <a href="http://status.dropbox.com">status.dropbox.com</a> for announcements about Dropbox service issues.</td></tr></table><h2>Endpoint-specific errors (409)</h2>The following table describes the top-level JSON object attributes present in the body of 409 responses.<table class="api-param-values center-first-col"><tr><th>Key</th><th>Description</th></tr><tr><td>error</td><td>A value that conforms to the error data type schema defined in the definition of each route.</td></tr><tr><td>error_summary</td><td>A string that summarizes the value of the "error" key. It is a concatenation of the hierarchy of union tags that make up the error. While this provides a human-readable error string, "error_summary" should not be used for programmatic error handling. To disincentive this, we append a random number of "." characters at the end of the string.</td></tr><tr><td>user_message</td><td>An optional field. If present, it includes a message that can be shown directly to the end user of your app. You should show this message if your app is unprepared to programmatically handle the error returned by an endpoint.</td></tr></table>
            </div>
            """

            sel = Selector(text=operation_html)
            sub_selectors = to_test.extractExtractorResults(sel, to_test.config.get('operation'))
            assert len(sub_selectors) == 2

            result = to_test.parse_paths(sel)
            endpoint_1 = result['/oauth2/token']
            endpoint_2 = result['/oauth2/authorize']

            def describe_basics_of_extraction():
                def it_should_have_one_operation():
                    assert len(endpoint_1) == 1
                    assert ['post'] == sorted(endpoint_1.keys())

                def describe_post_operation():
                    post_op = endpoint_1['post']

                    def it_should_return_parameter_types_with_no_qmark_and_states_required_field():
                        assert len(post_op['parameters']) == 5
                        print post_op['parameters'][2]
                        assert post_op['parameters'][2]['type'] == 'string'
                        assert post_op['parameters'][2]['in'] == 'query'
                        assert post_op['parameters'][2]['name'] == u'client_id'
                        assert post_op['parameters'][2]['required'] == False
                        assert post_op['parameters'][2]['description'] == "If credentials are passed in parameters, this parameter should be present and should be the app's key (found in the )."

                    def it_should_have_response_codes_with_global_error_codes():
                        assert len(post_op['responses']) == 7
                        assert ['200', '400', '401', '403', '409', '429', '500'] == sorted(post_op['responses'].keys())

                    def it_should_have_schema_for_the_200_response():
                        assert post_op['responses']['200']['schema'] == {'required': [u'access_token', u'account_id', u'token_type', u'uid'], 'type': 'object', 'properties': {u'access_token': {'type': 'string'}, u'token_type': {'type': 'string'}, u'account_id': {'type': 'string'}, u'uid': {'type': 'string'}}}

                    def it_should_have_details_for_the_global_responses():

                        assert post_op['responses']['400'] == {'description': 'Bad input parameter. The response body is a plaintext message with more information.'}
                        assert post_op['responses']['401'] == {'description': u'Bad or expired token. This can happen if the access token is expired or if the access token has been revoked by Dropbox or the user. To fix this, you should re-authenticate the user. The Content-Type of the response is JSON of type AuthError Example: invalid_access_token { "error_summary": "invalid_access_token/...", "error": { ".tag": "invalid_access_token" } } Example: invalid_select_user { "error_summary": "invalid_select_user/...", "error": { ".tag": "invalid_select_user" } } Example: invalid_select_admin { "error_summary": "invalid_select_admin/...", "error": { ".tag": "invalid_select_admin" } } Example: user_suspended { "error_summary": "user_suspended/...", "error": { ".tag": "user_suspended" } } Example: expired_access_token { "error_summary": "expired_access_token/...", "error": { ".tag": "expired_access_token" } } Example: other { "error_summary": "other/...", "error": { ".tag": "other" } } AuthError (open union) Errors occurred during authentication. This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. invalid_access_token Void The access token is invalid. invalid_select_user Void The user specified in \'Dropbox-API-Select-User\' is no longer on the team. invalid_select_admin Void The user specified in \'Dropbox-API-Select-Admin\' is not a Dropbox Business team admin. user_suspended Void The user has been suspended. expired_access_token Void The access token has expired.', 'schema': {'required': [u'error', u'error_summary'], 'type': 'object', 'properties': {u'error_summary': {'type': 'string'}, u'error': {'required': [u'.tag'], 'type': 'object', 'properties': {u'.tag': {'type': 'string'}}}}}}
                        assert post_op['responses']['403'] == {'description': u"The user or team account doesn't have access to the endpoint or feature. The Content-Type of the response is JSON of type AccessError AccessError (open union) Error occurred because the account doesn't have permission to access the resource. This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. invalid_account_type InvalidAccountTypeError Current account type cannot access the resource. InvalidAccountTypeError (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. endpoint Void Current account type doesn't have permission to access this route endpoint. feature Void Current account type doesn't have permission to access this feature. paper_access_denied PaperAccessError Current account cannot access Paper. PaperAccessError (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. paper_disabled Void Paper is disabled. not_paper_user Void The provided user has not used Paper yet."}
                        assert post_op['responses']['409'] == {'description': u'Endpoint-specific error. Look to the JSON response body for the specifics of the error.'}
                        assert post_op['responses']['429'] == {'description': u'Your app is making too many requests for the given user or team and is being rate limited. Your app should wait for the number of seconds specified in the "Retry-After" response header before trying again. The Content-Type of the response can be JSON or plaintext. If it is JSON, it will be type RateLimitError You can find more information in the data ingress guide . RateLimitError Error occurred because the app is being rate limited. This datatype comes from an imported namespace originally defined in the auth namespace. reason RateLimitReason The reason why the app is being rate limited. RateLimitReason (open union) This datatype comes from an imported namespace originally defined in the auth namespace. The value will be one of the following datatypes. New values may be introduced as our API evolves. too_many_requests Void You are making too many requests in the past few minutes. too_many_write_operations Void There are currently too many write operations happening in the user\'s Dropbox. retry_after UInt64 The number of seconds that the app should wait before making another request. The default for this field is 1.'}
                        assert post_op['responses']['500'] == {'description': u'An error occurred on the Dropbox servers. Check status.dropbox.com for announcements about Dropbox service issues.'}
            
            def describe_valid_schema():
                get_op = endpoint_2['get']

                def should_not_extract_url_as_schemas():
                    assert isinstance(get_op['responses']['200'], dict)
                    assert 'schema' not in get_op['responses']['200']
                    assert get_op['responses']['200'] == {'description': ''}

            def should_return_security_definitions():
                to_test.parse_apis_info(sel)
                oauth = to_test.swagger['securityDefinitions']["OAuth 2"]
                assert oauth["type"] == "oauth2"
                assert oauth["flow"] == "application"
                #assert oauth["authorizationUrl"] == "https://www.dropbox.com/oauth2/authorize"
                assert oauth["tokenUrl"] == "https://www.dropbox.com//oauth2/token"

        def should_parse_paths_with_global_attributes():
            item = result['/delete_manual_contacts_batch']['post']
            assert item['parameters'] == [{'in': 'query', 'type': u'string', 'name': u'email_addresses', 'description': u'List of manually added contacts to be deleted.'}]
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
            item = result['/delete_manual_contacts_batch']['post']
            assert '500' in item['responses']
            assert '5xx' not in item['responses']

        def describe_proper_parameter_types():

            def should_extract_proper_type_that_is_normal():
                item = result['/oauth2/authorize']['get']
                assert item['parameters'][0]['type'] == 'string'
                assert item['parameters'][0]['name'] == 'response_type'

            def should_extract_proper_type_that_has_parenthesis():
                item = result['/delete_manual_contacts_batch']['post']
                assert item['parameters'][0]['type'] == 'string'
                assert item['parameters'][0]['name'] == 'email_addresses'

                item = result['/update']['post']
                assert item['parameters'][0]['type'] == 'string'
                assert item['parameters'][0]['name'] == 'id'

                item = result['/token/from_oauth1']['post']
                assert item['parameters'][0]['type'] == 'string'
                assert item['parameters'][0]['name'] == 'oauth1_token'

            def should_extract_proper_type_that_has_question_mark():
                item = result['/templates/update_for_user']['post']
                assert item['parameters'][1]['type'] == 'string'
                assert item['parameters'][1]['name'] == 'name'

            def should_convert_list_to_string():
                item = result['/share_folder']['post']
                print item['parameters']
                assert item['parameters'][7]['name'] == 'actions'
                assert item['parameters'][7]['type'] == 'string'

            def should_convert_unknown_types_to_string():
                item = result['/get_temporary_upload_link']['post']
                assert item['parameters'][0]['name'] == 'commit_info'
                assert item['parameters'][0]['type'] == 'string'

            def should_convert_float_to_integer():
                item = result['/get_temporary_upload_link']['post']
                assert item['parameters'][1]['name'] == 'duration'
                assert item['parameters'][1]['type'] == 'integer'

            def should_convert_uint32_to_integer():
                item = result['/list_folder']['post']
                assert item['parameters'][6]['name'] == 'limit'
                assert item['parameters'][6]['type'] == 'integer'


        def describe_proper_parameter_names():
            resp = response_from('HTTP - Developers - Dropbox Business.html')
            result = to_test.parse_paths(resp)

            def should_extract_proper_name():
                item = result['/templates/update_for_team']['post']

                assert item['parameters'][3]['name'] == "add_fields"
