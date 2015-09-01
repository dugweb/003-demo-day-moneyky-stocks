import json
import codecs
from pprint import pprint

''' this short and simple recursive function will convert any decoded JSON object from using unicode strings to UTF-8-encoded byte strings'''

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

''' This function will read the raw JSON file and converts into a python object '''
def readjson(file):
    with codecs.open(file,'rU','utf-8') as data_file:
        data = json.load(data_file)
    data = byteify(data)
    #pprint(data)
    #pprint(data[0].keys()) # Gets the colums
    return data
