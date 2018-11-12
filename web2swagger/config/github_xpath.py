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
  'operations': {'selector': './/*[starts-with(@class,"content")]', 'type': 'xpath'},
  'operation': {'selector': 'h2', 'split': True, 'type': 'xpath'},
  # 'path': {'selector': './/pre[not(contains(@class, "highlight")) and not(contains(@class,"command-line"))]/code//text()', 'regex': r'\w+ (\/\S*)', 'type': 'xpath'},
  'path': {'selector': './/pre[not(contains(@class, "highlight")) and not(contains(@class,"command-line"))]/code//text()', 'regex': r'\w+ (.*\S\w+/?)', 'type': 'xpath'},
  'method': {'selector': './/pre[not(contains(@class, "highlight")) and not(contains(@class,"command-line"))]/code//text()', 'regex': r'(\w+) .*', 'type': 'xpath'},
  # 'method': {'selector': './/pre[not(contains(@class, "highlight")) and not(contains(@class,"command-line"))]/code//text()', 'regex': r'(\w+) .*/', 'type': 'xpath'},
  'parameters': {'selector': './/h3[contains(., "Parameters")]/following-sibling::table[1]', 'type': 'xpath'},
  'parameter': {'selector': './/tbody/tr', 'type': 'xpath'},
  'parameterName': {'selector': './td[1]//text()', 'regex': r'(\S+)', 'type': 'xpath'},
  'parameterType': {'selector': './td[2]//text()', 'regex': r'(array|string|integer|boolean)', 'type': 'xpath'},
  'parameterDescription': {'selector': './td[3]//text()', 'type': 'xpath'},
  'requestBody': {'selector': './/h4[contains(., "Example")]/following-sibling::pre[contains(@class, "highlight-json")]|.//h3[contains(., "Example")]/following-sibling::pre[contains(@class, "highlight-json")]', 'isExample': True, 'type': 'xpath'},
  'responses': {'selector': './/h3[contains(.,"Response")]|h4[contains(.,"Response")]', 'type': 'xpath'},
  'responseStatus': {'selector': './/pre[contains(@class, "highlight-headers")]', 'regex': r'Status: (\d+) ', 'sibling': True, 'type': 'xpath'},
  'responseDescription': {'selector': './/pre[contains(@class, "highlight-headers")]', 'regex': r'Status: \d+ (.*)', 'sibling': True, 'type': 'xpath'},
  'responseSchema': {'selector': './/pre[contains(@class, "highlight-json")]', 'isExample': True, 'sibling': True, 'type': 'xpath'},
  'defaultParameterLocations': {
    'put': 'field',
    'post': 'field',
    'patch': 'field',
  },
}

def fixPathParameters(path):
    pieces = path.split('/')
    new_pieces = []
    for p in pieces:
      if ':' in p:
        p = p.replace(':', '{') + '}'
      new_pieces.append(p)
    return '/'.join(new_pieces)
