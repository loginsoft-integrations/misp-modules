import json
import imdb

misperrors = {'error': 'Error'}
mispattributes = {'input': ['text'], 'output': ['text']}

# possible module-types: 'expansion', 'hover' or both
moduleinfo = {'version': '1', 'author': 'MISP',
              'description': 'Get the IMDB score of the movie title',
              'module-type': ['expansion', 'hover']}

# config fields that your code expects from the site admin
moduleconfig = []

ia = imdb.IMDb()

def getMovieID(movieTitle):
    movies = ia.search_movie(movieTitle)
    movieID = movies[0].movieID
    return movieID

def getScore(movieID):
    movie = ia.get_movie(movieID)
    score = movie.get('rating', 'Could not retreive rating')
    return score

def handler(q=False):
    if q is False:
        return False
    request = json.loads(q)

    movieTitle = request['text']
    movieID = getMovieID(movieTitle)
    score = getScore(movieID)

    r = {'results': [{'types': 'text', 'categories': ['Other'], 'values': score}]}
    return r


def introspection():
    return mispattributes


def version():
    moduleinfo['config'] = moduleconfig
    return moduleinfo

