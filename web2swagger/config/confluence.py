import re

config = {
  'url': 'https://docs.atlassian.com/ConfluenceServer/rest/6.12.0/',
  'urlRegex': r'^https:\/\/docs.atlassian.com\/ConfluenceServer\/rest\/6.12.0',
  'protocols': ['https'],
  'host': 'myhost:port',
  'basePath': '/rest/api',
  'title': 'Confluence REST API Documentation',
  'version': '6.12.0',
  'description': 'Confluence REST API Documentation',
  'operations': {'selector': '.resource'},
  'operation': {'selector': '.method'},
  'path': {'selector': 'h4 > code', 'regex': r'\w+ (.*\S\w+\}?)'},
  'method': {'selector': 'h4 > code', 'regex': r'(\w+) .*/'},
  'parameters': {'selector': 'h5:contains(Request) + h6:contains("query parameters") + table'},
  'parameter': {'selector': 'tr'},
  'parameterName': {'selector': 'td:first-of-type'},
  'parameterType': {'selector': 'td:nth-of-type(2)', 'regex': r'(array|string|int|boolean)'},
  'parameterDescription': {'selector': 'td:nth-of-type(3)'},
  'requestBody': {'selector': 'h5:contains(Request) ~ .representation-doc > .representation-doc-block > h6:contains(Schema) ~ pre > code'},
  'responses': {'selector': 'h5:contains(Responses) + ul > li > ul > li.representation'},
  'responseStatus': {'selector': '.representation-name > b', 'regex': r' (\d+)'},
  'responseDescription': {'selector': '.representation-name > i::text, .representation-doc:not(h6:contains(Example))::text'},
  'responseSchema': {'selector': '.representation-doc > .representation-doc-block > h6:contains(Schema) ~ pre > code'},
}

def fixPathString(path):
    path = path.replace('/rest/', '').strip()
    if not path.startswith('/'):
      path = '/' + path
    return path

def fixParameterType(type):
  if type == 'int' or type == 'long':
    type = 'integer'
  return type

def fixPathParameters(parameters):
    return parameters

config.update({'securityDefinitions': {
    'HTTP Basic': {
      'type': 'basic'
    }
  }
})
