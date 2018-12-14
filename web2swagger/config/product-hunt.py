config = {
  'url': 'https://api.producthunt.com/v1/docs/',
  'urlDocsPath': '/v1/docs/',
  'host': 'api.producthunt.com',
  'basePath': '/v1',
  'title': 'Product Hunt API',
  'description': {'selector': ''},
  'operation': {'selector': './/*[@class="api--content"]'},
  'path': {'selector': './/*[@class="api--request"]/pre[1]/text()', 'regex': r'/\w+ (.*)/'},
  'method': {'selector': './/*[@class="api--request"]/pre[1]/text()', 'regex': r'/(\w+) .*/'},
  'parameters': {'selector': 'table'},
  'parameter': {'selector': 'tr'},
  'parameterName': {'selector': 'td:first-of-type', 'regex': r'/(\w+)( required)?/'},
  'parameterDescription': {'selector': 'td:nth-of-type(2)'},
  'requestBody': {'selector': 'h3:nth-of-type(1) + h4 + pre + h4 + pre + h4 + pre', 'isExample': True},
  'responseStatus': {'selector': 'h3:nth-of-type(2) + h4 + pre', 'regex': r'/(\d+) .*/'},
  'responseDescription': {'selector': 'h3:nth-of-type(2) + h4 + pre', 'regex': r'/\d+ (.*)/'},
  'responseSchema': {'selector': 'h3:nth-of-type(2) + h4 + pre + h4 + pre + h4 + pre', 'isExample': True},
  'defaultParameterLocations': {
      'put': 'field',
      'post': 'field',
      'patch': 'field',
    }
}

def fixPathString(path):
  pieces = path.split('/')
  params = []

  for piece in pieces:
      match = piece.match(r'/^(\d+)$/') or piece.match('/l33thaxor/')
      if match:
          path = path.replace('/' + match[0], '/{id}')
      if piece == 'games' or piece == 'tech' or piece == 'books' or piece == 'podcasts':
          path = path.replace(piece, '{category}')

  return path
