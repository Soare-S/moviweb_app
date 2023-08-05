import json
import requests
API_KEY = "1b44b07a"
SECRET_KEY = 'forza'


def get_movie_data(title):
    """Get movie data from the OMDB API by providing the movie title."""
    try:
        api_url = f'https://www.omdbapi.com/?t={title}&apikey={API_KEY}'
        response = requests.get(api_url)
        text_response = response.text
        json_response = json.loads(text_response)
        return json_response
    except requests.RequestException:
        return {"Error": "No internet"}