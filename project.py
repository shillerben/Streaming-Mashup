from flask import Flask, render_template, request, jsonify
import urllib.parse
import requests
import json

app = Flask(__name__)

mode = "DEV"
#mode = 'PROD'

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/result/<movie>')
def result(movie):
    # utelly api call
    query = urllib.parse.urlencode({"term": movie, "country": "us"})
    url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup?" + query
    headers={
      "X-RapidAPI-Host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
      "X-RapidAPI-Key": "f5785d17ecmsh292914dc61cf9a1p1a7434jsna1e418f64f4c"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        return render_template('not_found.html')
    utelly_json = response.json()
    first_result = utelly_json["results"][0]
    title = first_result["name"]
    if len(utelly_json["results"]) > 0:
        locations = first_result["locations"]
    else:
        locations = []

    query = urllib.parse.urlencode({"apikey": "c667890", "t": movie})
    url = "http://www.omdbapi.com/?" + query

    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return render_template('not_found.html')
    omdb_json = response.json()
    year = omdb_json["Year"]
    poster_url = omdb_json["Poster"]


    return render_template('result.html', title=title, poster_url=poster_url, locations=locations, year=year)
    


if __name__ == "__main__":
    if mode == 'DEV':
        app.run(host='0.0.0.0', debug=True, port=5000)
    else:
        app.run(host='0.0.0.0', port=80)
