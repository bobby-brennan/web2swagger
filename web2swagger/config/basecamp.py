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
    'put': 'field'
  },
}

def fixPathString(path):
    pieces = path.split('/')
    new_pieces = []
    for idx, x in enumerate(pieces):
      if 'CHATBOT_KEY' in x:
        x = 'chatbotKey'
      if ':' in x:
        new_pieces.append('{%s}' % x.replace(':', '').strip())
      else:
        key_splits = x.split('.')
        key = key_splits[0]
        if is_number(key):
          prev_idx = idx - 1
          if prev_idx >= 0:
            prev_text = pieces[prev_idx]
            if prev_text.endswith('s'):
              prev_text = prev_text[:-1]
            newKey = '{%sId}%s' % (prev_text, '.' + key_splits[1] if len(key_splits) > 1 else '')
            new_pieces.append(newKey.strip())
            continue
        new_pieces.append(x)
    return '/'.join(new_pieces)

def fixPathSchema(schema_data):
  if isinstance(schema_data, dict) and 'required' in schema_data and isinstance(schema_data['required'], list):
    schema_data.pop('required', None)
    
  if isinstance(schema_data, list):
      for idx, x in enumerate(schema_data):
        fixPathSchema(schema_data[idx])
  if isinstance(schema_data, dict):
      for x, data in schema_data.items():
        fixPathSchema(schema_data[x])
  return schema_data

def is_number(nbr_txt):
  result = False
  try:
    int(nbr_txt)
    result = True
  except:
    pass
  return result

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
      "authorizationUrl": "https://launchpad.37signals.com/authorization/new?type=web_server",
      "tokenUrl": "https://launchpad.37signals.com/authorization/token?type=web_server"
    }
  }
})

