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
  'operation': [{'selector': '.method-title', 'split': True}, {'selector': './/*[@class="documentation__routes"]/div/*[@class="section toc-el"][contains(.//dt[contains(text(),"Endpoint format")]/following-sibling::dd[1]/a/text(), "RPC")]', 'type': 'xpath'}],
  'operationDescription': {'selector': './/*[@class="method-title"]/following-sibling::dl[1]/dt[text()="Description"]/following-sibling::dd[1]//text()|./dl[@class="documentation__route-items"][last()]/dt[text()="Description"]/following-sibling::dd[1]//text()', 'type': 'xpath'},
  'endPointFormat': {'selector': './dl[@class="documentation__route-items"][last()]/dt[contains(text(),"Endpoint format")]/following-sibling::dd[1]//text()', 'type': 'xpath'},
  'path': {'selector': './/h3[@class="method-title"]/text()|./preceding-sibling::h2[1]/text()|./h3/text()', 'type': 'xpath', 'join': '/'},
  'method': {'selector': 'dl:first-of-type dt:contains(Method) + dd, dl:first-of-type dd > pre.documentation__curl-example', 'regex': r'(POST|GET|PUT|DELETE)', 'default': 'POST'},
  'parameters': {'selector': './/*[@class="method-title"]/following-sibling::dl[1]/dt[contains(text(),"Parameters")]/following-sibling::dd[1]|./dl[@class="documentation__route-items"][last()]/dt[contains(text(),"Parameters")]/following-sibling::dd[1]', 'type': 'xpath'},
  'parameter': {'selector': './/*[@class="field"][not(ancestor::*[@class="nested-child collapse"])]', 'type': 'xpath'},
  'parameterName': {'selector': './*[1]/following-sibling::i[1]/preceding-sibling::*[1]//text()', 'type': 'xpath'},
  'parameterType': {'selector': 'i'},
  'parameterDescription': {'selector': '.field::text'},
  'responses': {'selector': 'dl dt:contains(Returns) + dd > pre.literal-block, dl dt:contains(Returns) + dd > div > pre.literal-block'},
  'responseStatus': '200',
  'responseDescription': '',
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

def fixPathString(path):
    path = path.replace('//', '/').strip()
    if not path.startswith('/'):
      path = '/' + path
    return path

def fixParameterType(type):
    pieces = type.split()
    temp_type = pieces[0]
    pieces = temp_type.split('(')
    new_type = pieces[0].strip()
    return new_type

def fixPathSchema(schema_data):
  return schema_data

config.update({'securityDefinitions': {
    'OAuth 2': {
      'type': 'oauth2',
      'flow': 'application',
      "authorizationUrl": "https://www.dropbox.com/1/oauth2/authorize",
      "tokenUrl": "https://api.dropbox.com/1/oauth2/token",
      'scopes': {}
    }
  }
})
