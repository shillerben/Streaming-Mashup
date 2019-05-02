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
    walmartLink = "https://www.walmart.com/search/?cat_id=0&query="+query
    amazonLink="https://www.amazon.com/s?k="+query
    BBLink="https://www.bestbuy.com/site/searchpage.jsp?st="+query
    shoppingLinks = {walmart : walmartLink, amazon : amazonLink, bestBuy: BBLink}
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



    return render_template('result.html', title=movie_title, poster_url=poster_url, locations=locations, year=year, rating = movie_rating, runtime = movie_runtime, plot = movie_plot, genre = movie_genre, reviews = movie_reviews, actors = movie_actors, website = movie_website, director = movie_director, walmart = walmartLink, bestBuy = BBLink, amazon = amazonLink)



if __name__ == "__main__":
    if mode == 'DEV':
        app.run(host='0.0.0.0', debug=True, port=5000)
    else:
        app.run(host='0.0.0.0', port=80)
