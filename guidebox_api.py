import guidebox
import json
import requests
from ast import literal_eval

# this program was used to fill our movieList for autocomplete

# ****** NOTE: we are limited to 1000 free calls ***********
key = "f3314444637db1c98eb8812319820aab68ea8065"
guidebox.api_key = key
movies = guidebox.Movie.list(limit=250)
movieString = movies.__str__()
#io = StringIO('["streaming API"]')
movieList = json.loads(movieString)
#print(movieString)
#print(type(movieList)) # tpye = dict
for i in movieList["results"]:
    #print("i type: ")
    #print( type(i) ) # i is a dict
    #print(i)
    print("\""+i["title"]+"\",")
    #for n in i:
        #print("i at "+ n)
        #print("n type: ")
        #print(type(n)) # n is a string
