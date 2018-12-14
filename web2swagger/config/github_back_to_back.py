import re

config = {
  'url': 'https://developer.github.com/v3',
  'urlRegex': r'/^https:\/\/developer.github.com\/v3/',
  'urlDocsPath': '/v3/',
  'protocols': ['https'],
  'host': 'api.github.com',
  'basePath': '/',
  'title': 'GitHub API',
  'version': 'v3',
  'description': 'The GitHub API',
  'operations': {'selector': '.content'},
  'operation': {'selector': 'h2', 'split': True},  # was: 'h2 ~ pre:not(.highlight)'
  'path': {'selector': 'pre:not(.highlight):not(.command-line) > code', 'regex': r'\w+ (\/\S*)'},
  'method': {'selector': 'pre:not(.highlight):not(.command-line) > code', 'regex': r'(\w+) .*'},
  'parameters': {'selector': 'h3:contains(Parameters) + table'},
  'parameter': {'selector': 'tbody tr'},
  'parameterName': {'selector': 'td:first-of-type', 'regex': r'(\S+)'},
  'parameterType': {'selector': 'td:nth-of-type(2)', 'regex': r'(array|string|integer|boolean)'},
  'parameterDescription': {'selector': 'td:nth-of-type(3)'},
  'requestBody': {'selector': 'h4:contains(Example) ~ pre.highlight-json, h3:contains(Example) ~ pre.highlight-json', 'isExample': True},
  'responses': {'selector': 'h3:contains(Response), h4:contains(Response)'},
  'responseStatus': {'selector': 'pre.highlight-headers', 'regex': r'Status: (\d+) ', 'sibling': True},
  'responseDescription': {'selector': 'pre.highlight-headers', 'regex': r'Status: \d+ (.*)', 'sibling': True},
  'responseSchema': {'selector': 'pre.highlight-json', 'isExample': True, 'sibling': True},
}

def fixPathString(path):
    pieces = path.split('/')
    new_pieces = []
    for p in pieces:
      if ':' in p:
        p = p.replace(':', '{') + '}'
      new_pieces.append(p)
    return '/'.join(new_pieces)

def fixPathParameters(parameters):
    return parameters
