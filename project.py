from flask import Flask, render_template, request, jsonify
import datetime
import urllib.parse
import requests
import json
import socket

app = Flask(__name__)

mode = "DEV"
#mode = 'PROD'
def get_lat_lon(ipaddr):
    if mode == 'PROD':
        url = "http://ip-api.com/json/" + str(ipaddr)
        response = requests.get(url)
        response_json = response.json()
        lat = response_json["lat"]
        lon = response_json["lon"]
    else:
        lat = 30.620556
        lon = -96.343056
    return (lat, lon)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/result/<movie>')
def result(movie):
    if mode == 'PROD':
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        ip = "50.24.110.76"
    (lat, lon) = get_lat_lon(ip)
    query = urllib.parse.urlencode({"apikey": "c667890", "t": movie,"Plot":"full"})
    url = "http://www.omdbapi.com/?" + query

    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return render_template('not_found.html')
    omdb_json = response.json()
    year = omdb_json["Year"]
    poster_url = omdb_json["Poster"]
    movie_rating = omdb_json["Rated"]
    movie_runtime = omdb_json["Runtime"]
    movie_plot = omdb_json["Plot"]
    movie_genre = omdb_json["Genre"]
    movie_reviews = omdb_json["Ratings"]
    movie_actors = omdb_json["Actors"]
    movie_website = omdb_json["Website"]
    movie_director = omdb_json["Director"]
    movie_title = omdb_json["Title"]
    searchTitle = movie_title.replace(" ", "+")
    walmart = "https://www.walmart.com/search/?cat_id=0&query="+searchTitle
    amazon="https://www.amazon.com/s?k="+searchTitle
    bestBuy="https://www.bestbuy.com/site/searchpage.jsp?st="+searchTitle
    #shoppingLinks = {walmart : walmartLink, amazon : amazonLink, bestBuy: BBLink}
    # utelly api call
    query = urllib.parse.urlencode({"term": movie_title, "country": "us"})
    url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup?" + query
    headers={
      "X-RapidAPI-Host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
      "X-RapidAPI-Key": "f5785d17ecmsh292914dc61cf9a1p1a7434jsna1e418f64f4c"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        return render_template('not_found.html')
    utelly_json = response.json()
    if len(utelly_json["results"]) == 0:
        locations = []
    else:
        first_result = utelly_json["results"][0]
        #title = first_result["name"]
        locations = first_result["locations"]

    # -----------------------------------------------------------------------------
    # movieglu api (getting glu_id)
    now = datetime.datetime.now().isoformat(timespec="milliseconds")
    location = str(lat) + ";" + str(lon)
    headers = {"api-version": "v200", "Authorization": "Basic U0NIT18xMDoxbFhJaFpNMzlod08=", "x-api-key": "AFvdDRsfgU1z0UdFCYdDo6584GlekAKJ7sFHuLzW", "device-datetime": now, "territory": "US", "client": "SCHO_10"}
    query = urllib.parse.urlencode({"query": movie, "n": "1"})
    url = "https://api-gate2.movieglu.com/filmLiveSearch/?" + query

    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        return render_template('not_found.html')
    movieglu_json = response.json()
    glu_id = movieglu_json["films"][0]["film_id"]

    # getting showtimes based on glu_id
    headers = {"api-version": "v200", "Authorization": "Basic U0NIT18xMDoxbFhJaFpNMzlod08=", "x-api-key": "AFvdDRsfgU1z0UdFCYdDo6584GlekAKJ7sFHuLzW", "device-datetime": now, "territory": "US", "client": "SCHO_10", "geolocation": location}
    today = datetime.date.today().isoformat()
    query = urllib.parse.urlencode({"film_id": glu_id, "date": today})
    url = "https://api-gate2.movieglu.com/filmShowTimes/?" + query

    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        return render_template('not_found.html')
    movieglu_json2 = response.json()
    cinemas = movieglu_json2["cinemas"]

    return render_template('result.html', title=movie_title, poster_url=poster_url, locations=locations, year=year, rating=movie_rating, runtime=movie_runtime, plot=movie_plot, genre=movie_genre, reviews=movie_reviews, actors=movie_actors, website=movie_website, director=movie_director, walmart=walmart, bestBuy=bestBuy, amazon=amazon, cinemas=cinemas)



if __name__ == "__main__":
    if mode == 'DEV':
        app.run(host='0.0.0.0', debug=True, port=5000)
    else:
        app.run(host='0.0.0.0', port=80)
