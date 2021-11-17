from os import listdir
from os.path import isfile, join
from pprint import pprint

basePath = """//alexandria.rutgers.edu/makerspace-shared/!3D Prints/"""


def produceUsers():
    return [x for x in listdir(basePath) if not isfile(x)]


def produceUserSubmissions(userString):
    return [x for x in listdir(join(basePath, userString)) if not isfile(x)]
