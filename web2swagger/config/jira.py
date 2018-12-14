import re

config = {
  'url': 'https://docs.atlassian.com/DAC/rest/jira/6.1.html',
  'urlRegex': r'^https:\/\/docs.atlassian.com\/DAC\/rest/',
  'protocols': ['https'],
  'host': 'jira.atlassian.com',
  'basePath': '/rest/api/2',
  'title': 'JIRA REST API',
  'version': '6.1',
  'description': 'JIRA 6.1 REST API documentation',
  'operations': {'selector': '.resource'},
  'operation': {'selector': '.method',},
  'operationDescription': {'selector': 'h4 + p:first-of-type'},
  'path': {'selector': './ancestor::*[@class="resource"]/h3/text()', 'type': 'xpath'},
  'method': {'selector': 'h4::text', 'regex': r'(POST|GET|DELETE|PUT)'},
  'parameters': {'selector': './h6[contains(text(), "request query parameters")]/following-sibling::table[1]|./ancestor::*[@class="resource"]/h6[contains(., "resource-wide template parameters")]/following-sibling::table[1]', 'type': 'xpath'},
  'parameter': {'selector': 'tr'},
  'parameterName': {'selector': 'td:first-of-type'},
  'parameterType': {'selector': 'td:nth-of-type(2)', 'regex': r'(string|int|boolean|long)'},
  'parameterDescription': {'selector': 'td:nth-of-type(3)'},
  'requestBody': {'selector': 'p:contains("acceptable request representations:") + ul > li > .toggle > h6:contains(Example) ~ pre > code', 'isExample': True},
  'responses': {'selector': 'p:contains("available response representations:") + ul > li'},
  'responseStatus': {'selector': 'div:first-of-type', 'regex': r'(\d+)', 'default': '200'},
  'responseDescription': {'selector': '.toggle p'},
  'responseSchema': {'selector': 'h6:contains(Example) ~ pre > code', 'isExample': True},
  'defaultParameterLocations': {
    'put': 'query',
    'post': 'query',
    'patch': 'query',
  },
}

def fixPathString(path):
  return path

def fixParameterType(type):
  if type == 'int' or type == 'long':
    type = 'integer'
  return type

def fixPathParameters(parameters):
    return parameters

def fixPathSchema(schema_data):
  return schema_data

config.update({'securityDefinitions': {
    'HTTP Basic': {
      'type': 'basic'
    }
  }
})
  