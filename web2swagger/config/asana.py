import re

config = {
  'url': 'https://asana.com/developers/api-reference',
  'urlRegex': r'^https:\/\/asana.com\/developers\/api-reference',
  'protocols': ['https'],
  'host': 'app.asana.com',
  'basePath': '/api/1.0',
  'title': 'ASANA Developers API',
  'description': 'ASANA Developers API',
  'operations': {'selector': '.tab-content'},
  'operation': {'selector': 'pre[code/@class="nohighlight"]', 'split': True, 'type': 'xpath'},
  'operationDescription': {'selector': './/p[1]//text()', 'type': 'xpath'},
  'path': {'selector': 'pre:first-of-type > code::text', 'regex': r'\w+ (.*\S\w+\}?)'},
  'method': {'selector': 'pre:first-of-type > code::text', 'regex': r'(\w+) .*'},
  'parameters': {'selector': 'pre:first-of-type ~ table'},
  'parameter': {'selector': 'tbody tr'},
  'parameterName': {'selector': 'td:first-of-type'},
  'parameterDescription': {'selector': 'td:nth-of-type(2)::text'},
  'parameterRequired': {'selector': 'td:nth-of-type(2) > strong'},
  'parameterReadOnly': {'selector': 'td:nth-of-type(2) > strong'}, 
  'responses': {'selector': 'pre > code:contains("# Response")'},
  'responseStatus': {'selector': 'code', 'regex': r'( \d+)\s\{'},
  'responseSchema': {'selector': 'code', 'regex': r'(\{(\s*.+?\s)*\})', 'isExample': True},
  'globalExtractors': {
    'parameters': {'selector': 'h5[id^="fields"] + table'},
    'parameter': {'selector': 'tbody tr'},
    'parameterName': {'selector': 'td:first-of-type'},
    'parameterDescription': {'selector': 'td:nth-of-type(2)::text'},
    'parameterRequired': {'selector': 'td:nth-of-type(2) > strong'},
    'parameterReadOnly': {'selector': 'td:nth-of-type(2) > strong'}, 
  },
}

def fixPathString(path):
    return path

def fixPathParameters(parameters):
    for param in parameters:
      param.pop('required', None)
    return parameters

config.update({'securityDefinitions': {
    'OAuth 2': {
      'type': 'oauth2',
      'flow': 'accessCode',
      "authorizationUrl": u"https://app.asana.com/-/oauth_authorize",
      "tokenUrl": u"https://app.asana.com/-/oauth_token",
      "scopes": {
        "default": u"Provides access to all endpoints documented in our API reference. If no scopes are requested, this scope is assumed by default.",
        "openid": u"Provides access to OpenID Connect ID tokens and the OpenID Connect user info endpoint.",
        "email": u"Provides access to the users email through the OpenID Connect user info endpoint.",
        "profile": u"Provides access to the users name and profile photo through the OpenID Connect user info endpoint."
      }
    }
  }
})
