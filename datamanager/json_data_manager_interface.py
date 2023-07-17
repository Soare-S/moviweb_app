import json
import requests
from .data_manager_interface import DataManagerInterface


API_KEY = "1b44b07a"


def write_info_to_file(filename, info):
    """Write posts to the JSON file."""
    try:
        with open(filename, 'w') as file:
            json.dump(info, file, indent=4)
    except IOError as e:
        print(f"Error writing posts to file: {e}")


def get_movie_data(title):
    try:
        api_url = f'https://www.omdbapi.com/?t={title}&apikey={API_KEY}'
        response = requests.get(api_url)
        text_response = response.text
        json_response = json.loads(text_response)
        return json_response
    except requests.RequestException:
        return {"Error": "No internet"}


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return all the users information
        with open(self.filename) as file:
            data = json.load(file)
            users = data["users"]
        return users

    def get_user_movies(self, user_id):
        # Return all the movies for a given user
        users = self.get_all_users()
        movies = users[str(user_id)]["movies"]
        return movies

    def list_all_users(self):
        users_data = self.get_all_users()
        users_list = []
        for user_id, user in users_data.items():
            user = {
                "id": user_id,
                "name": user["name"]
            }
            users_list.append(user)
        return users_list

    def get_movie(self, user_id, movie_id):
        data = self.get_user_movies(user_id)
        for movie in data:
            if movie["id"] == movie_id:
                return movie

    def delete_movie(self, user_id, movie_id):
        movies_info = self.get_user_movies(user_id)
        data = self.get_all_users()
        for index, movie in enumerate(movies_info):
            if movie["id"] == movie_id:
                movies_info.pop(index)
                break
        data[user_id]["movies"] = movies_info
        updated_info = {
            "users": data
        }
        write_info_to_file("movies.json", updated_info)

    def user_exist(self, name):
        data = self.get_all_users()
        for user_data in data.values():
            if user_data["name"] == name:
                return True
        return False

    def movie_exist(self, title, user_id):
        data = self.get_user_movies(user_id)
        for movie in data:
            if title in movie["title"]:
                return True
        return False

    def add_user(self, name):
        data = self.get_all_users()
        user_id = max(int(users_id) for users_id in data.keys()) + 1
        data[f"{user_id}"] = {
            "name": name,
            "movies": []
        }
        updated_info = {
            "users": data
        }
        write_info_to_file("movies.json", updated_info)

    def add_movie(self, user_id, title):
        data = self.get_all_users()
        movie_info = get_movie_data(title)
        if len(movie_info) < 3:
            return "Not found"
        else:
            print(movie_info)
            movie_id = movie_info["imdbID"]
            movie_name = movie_info["Title"]
            director = movie_info["Director"]
            year = movie_info["Year"]
            rating = movie_info["imdbRating"]
            poster = movie_info["Poster"]
            link = f"https://www.imdb.com/title/{movie_id}/"
            movie = {
                "id": movie_id,
                "title": movie_name,
                "director": director,
                "year": int(year),
                "rating": float(rating),
                "poster": poster,
                "link": link
            }
            data[str(user_id)]["movies"].append(movie)
            updated_info = {
                "users": data
            }
            write_info_to_file("movies.json", updated_info)

    def update_movie(self, user_id, movie_id, title, director, year, rating):
        data = self.get_all_users()
        movies = data[str(user_id)]["movies"]
        for index, movie in enumerate(movies):
            if movie["id"] == movie_id:
                movie["title"] = title
                movie["director"] = director
                movie["year"] = int(year)
                movie["rating"] = float(rating)
                data[str(user_id)]["movies"][index] = movie
        updated_info = {
            "users": data
        }
        write_info_to_file("movies.json", updated_info)

