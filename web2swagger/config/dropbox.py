import re

config = {
  'url': 'https://www.dropbox.com/developers',
  'urlRegex': r'^https:\/\/www.dropbox.com\/developers/documentation',
  'protocols': ['https'],
  'host': 'api.dropboxapi.com',
  'basePath': '/2',
  'title': 'Dropbox API',
  'version': 'v2',
  'description': 'Dropbox API',
  'operations': {'selector': '.documentation'},
  'operation': {'selector': '.method-title, .documentation__routes > div > [class^="section toc-el"]', 'split': True},
  'path': {'selector': 'h3'},
  'method': {'selector': 'dl dt:contains(Method) + dd, dl dd > pre.documentation__curl-example', 'regex': r'(POST|GET|PUT|DELETE)'},
  'parameters': {'selector': 'dl dt:contains(Parameters) + dd'},
  'parameter': {'selector': './/*[@class="field"][not(ancestor::*[@class="nested-child collapse"])]', 'type': 'xpath'},
  'parameterName': {'selector': './*[1]/following-sibling::i[1]/preceding-sibling::*[1]//text()', 'type': 'xpath'},
  'parameterType': {'selector': 'i'},
  'parameterDescription': {'selector': '.field::text'},
  'responses': {'selector': 'dl dt:contains(Returns) + dd > pre.literal-block, dl dt:contains(Returns) + dd > div > pre.literal-block'},
  'responseStatus': '200',
  'responseDescription': {'selector': '* + div'},
  'responseSchema': {'selector': 'pre.literal-block', 'isExample': True},
  'globalExtractors': {
    'responses': {'selector': '.documentation > *[id="error-handling"] > h2:contains("Errors by status code") + table > tr'},
    'responseStatus': {'selector': 'td:first-of-type'},
    'responseDescription': {'selector': 'td:nth-of-type(2)'},
    'responseSchema': {'selector': 'td:nth-of-type(2) pre.literal-block', 'isExample': True},
  },

  'defaultParameterLocations': {
    'put': 'field',
    'post': 'field',
    'patch': 'field',
  },
}

def fixPathParameters(path):
    return path

def fixParameterType(type):
    pieces = type.split()
    temp_type = pieces[0]
    pieces = temp_type.split('(')
    new_type = pieces[0].strip()
    return new_type

config.update({'securityDefinitions': {
    'OAuth 2': {
      'type': 'oauth2',
      'flow': 'application',
      #"authorizationUrl": "https://www.dropbox.com/oauth2/authorize",
      "tokenUrl": "https://www.dropbox.com//oauth2/token",
    }
  }
})