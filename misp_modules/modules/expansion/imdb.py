import json
import imdb

misperrors = {'error': 'Error'}
mispattributes = {'input': ['text'], 'output': ['text']}

# possible module-types: 'expansion', 'hover' or both
moduleinfo = {'version': '1', 'author': 'MISP',
              'description': 'Get the IMDB score of the movie title',
              'module-type': ['hover']}

# config fields that your code expects from the site admin
moduleconfig = []

ia = imdb.IMDb()

def handler(q=False):
    if q is False:
        return False
    request = json.loads(q)

    movieTitle = request['text']
    movies = ia.search_movie(movieTitle)
    movieID = movies[0].movieID
    movie = ia.get_movie(movieID)
    score = movie.get('rating', 'Could not retreive rating')

    r = {'results': [{'types': 'text', 'values': score}]}
    return r


def introspection():
    return mispattributes


def version():
    moduleinfo['config'] = moduleconfig
    return moduleinfo
