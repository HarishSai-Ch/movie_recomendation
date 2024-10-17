from flask import Flask, render_template, request, redirect
import random
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__) 

TMDB_API_KEY = os.getenv('TMDB_API_KEY')  # Fetch the API key from the environment variables


@app.route('/')
def home():
    url = 'https://api.themoviedb.org/3/discover/movie?api_key={}&language=en-US&with_original_language={}'.format(TMDB_API_KEY,"te")
    response = requests.get(url)
    movies = response.json().get('results', [])
    return render_template('home.html', movies=movies[:18],lan="Telugu",home=True)



@app.route('/hollywood-movies', methods=['POST'])
def english_movies():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    data = response.json()
    movies = data['results']  # Extract the list of movies
    return render_template('home.html', movies=movies[:18],lan="English",home=False)


@app.route('/bollywood-movies', methods=['POST'])
def hindi_movies():
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&with_original_language=hi'
    response = requests.get(url)
    data = response.json()
    movies = data['results']  # Extract the list of movies
    print(len(movies))
    filter_mvs=[]
    for m in movies:
        if m["overview"]!='':
            filter_mvs.append(m)
    return render_template('home.html', movies=filter_mvs[:18],lan="Hindi",home=False)

@app.route('/search', methods=['POST'])
def search_movie():
    query = request.form.get('query')
    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}'
    response = requests.get(url)
    data = response.json()
    movies = data['results']  # Extract the list of movies
    return render_template('search_details.html', movies=movies[:18],result=query,home=False)


@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US'
    response = requests.get(url)
    movie = response.json()
    
    # Get the trailer information
    video_url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=en-US'
    video_response = requests.get(video_url)
    videos = video_response.json().get('results', [])
    
    trailer_key = None
    for video in videos:
        if video['type'] == 'Trailer':
            trailer_key = video['key']
            break

    return render_template('movie_detail.html', movie=movie, trailer_key=trailer_key)



if __name__=='__main__':
    app.run(debug=True)