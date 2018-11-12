import re

config = {
  'url': 'https://github.com/basecamp/bc3-api',
  'urlRegex': r'^https:\/\/github.com\/basecamp\/bc3-api\/blob\/master\/sections\/',
  'protocols': ['https'],
  'host': '3.basecampapi.com',
  'basePath': '/999999999',
  'title': 'The Basecamp 3 API',
  'version': 'bc3-api',
  'description': 'The Basecamp 3 API',
  'operations': {'selector': 'article'},
  'operation': {'selector': 'h2', 'split': True},
  'path': {'selector': 'ul li > code:first-of-type', 'regex': r'\w+ (.*\S\w+/?)'},
  'method': {'selector': 'ul li > code:first-of-type', 'regex': r'(\w+) .*'},
  'parameters': {'selector': 'p:contains("Required parameters"), p:contains("Required URI query parameters")'},
  'parameter': {'selector': 'code', 'split': True},
  'parameterName': {'selector': 'code'},
  'parameterDescription': {'selector': ' '},
  'requestBody': {'selector': 'h6:contains("Example JSON Request") + .highlight-source-json > pre', 'isExample': True},
  'responses': {'selector': 'h6:contains("Example JSON Response"), p:contains("This endpoint will return"), p:contains("Returns ")'},
  'responseStatus': {'selector': 'code:first-of-type', 'default': '200', 'regex': r'(\d+)'},
  'responseDescription': {'selector': 'code:first-of-type', 'regex': r'\d+ (.*)'},
  'responseSchema': {'selector': '.highlight-source-json > pre', 'sibling': True, 'isExample': True},

  'defaultParameterLocations': {
    'put': 'field',
    'post': 'field',
    'patch': 'field',
  },
}

def fixPathParameters(path):
    pieces = path.split('/')
    new_pieces = []
    for x in pieces:
      if ':' in x:
        new_pieces.append('{%s}' % x.replace(':', '').strip())
      else:
        new_pieces.append(x)
    return '/'.join(new_pieces)

config.update({'securityDefinitions': {
    'ApiKeyAuth': {
      'type': 'apiKey',
      'in': 'header',
      'name': 'ACCESS_TOKEN',
      "description": "a bearer token, including the prefix 'Bearer', e.g. 'Bearer abcde'"
    },
    'OAuth 2': {
      'type': 'oauth2',
      'flow': 'accessCode',
      "authorizationUrl": "https://launchpad.37signals.com/authorization/new",
      "tokenUrl": "https://launchpad.37signals.com/authorization/token"
    }
  }
})
