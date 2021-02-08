import json
import imdb
from pymisp import MISPEvent, MISPObject

from . import check_input_attribute, standard_error_message

misperrors = {'error': 'Error'}
mispattributes = {'input': ['text'], 'format': 'misp_standard'}

# possible module-types: 'expansion', 'hover' or both
moduleinfo = {'version': '1', 'author': 'MISP',
              'description': 'Get the details of a movie title from IMDB as a MISP-Object',
              'module-type': ['expansion', 'hover']}

# config fields that your code expects from the site admin
moduleconfig = ['apikey']

ia = imdb.IMDb()

def getDetails(movieTitle):
    movies = ia.search_movie(movieTitle)
    movie = movies[0]
    details = {
        'title': movie.get('title', ''),
        'long title': movie.get('long imdb title', ''),
        'year': movie.get('year', ''),
        'cover': movie.get('cover', ''),
    }
    return details

def createMISPEvent(details, attributeUUID, apikey):
    misp_event = MISPEvent()

    misp_object = MISPObject('movie-details')
    for k, v in details.items():
        if k == 'cover':
            misp_object.add_attribute(k, type='link', value=v)
        else:
            misp_object.add_attribute(k, type='text', value=v, comment=f'Using API Key: {apikey}')

    misp_object.add_reference(attributeUUID, 'expanded-from')
    misp_event.add_object(misp_object)
    return misp_event

def handler(q=False):
    if q is False:
        return False
    request = json.loads(q)

    config = request.get("config", {})
    apikey = config.get("apikey", None)

    # Input sanity check
    if not request.get('attribute') or not check_input_attribute(request['attribute']):
        return {'error': f'{standard_error_message}, which should contain at least a type, a value and an uuid.'}
    movieAttribute = request['attribute']
    if movieAttribute['type'] not in mispattributes['input']:
        return {'error': 'Unsupported attribute type.'}

    # Get details from IMDB API
    movieTitle = movieAttribute['value']
    details = getDetails(movieTitle)

    # Use PyMISP to create compatible MISP Format
    misp_event = createMISPEvent(details, movieAttribute['uuid'], apikey)

    # Avoid serialization issue
    event = json.loads(misp_event.to_json())

    results = {'Object': event['Object']}
    return {'results': results}


def introspection():
    return mispattributes


def version():
    moduleinfo['config'] = moduleconfig
    return moduleinfo
