import json
import requests
import uuid
import os
import bcrypt
from configuration.key import API_KEY
from .data_manager_interface import DataManagerInterface


def write_data_to_json_file(filename, info):
    """Write posts to the JSON file."""
    try:
        file_path = os.path.join("data", filename)
        with open(file_path, 'w') as file:
            json.dump(info, file, indent=4)
    except IOError as e:
        print(f"Error writing posts to file: {e}")


def get_movie_data(title):
    """Get movie data from the OMDB API by providing the movie title."""
    try:
        lower_title = title.lower()
        capitalized_title = lower_title.capitalize()
        api_url = f'https://www.omdbapi.com/?t={capitalized_title}&apikey={API_KEY}'
        response = requests.get(api_url)
        text_response = response.text
        json_response = json.loads(text_response)
        return json_response
    except requests.RequestException:
        return {"Error": "No internet"}


class JSONDataManager(DataManagerInterface):
    # Initialize the data manager with the JSON file name
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return all the users information from the JSON file
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
        for user_id, user_data in users_data.items():
            try:
                password = user_data["password"]
                if password:
                    continue
            except KeyError:
                pass
            user = {
                "id": user_id,
                "name": user_data["name"],
                'number': len(user_data['movies'])
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
        write_data_to_json_file("movies.json", updated_info)

    def user_exist(self, name):
        data = self.get_all_users()
        for user_data in data.values():
            if user_data["name"] == name:
                return True
        return False

    def movie_exist(self, title, user_id):
        data = self.get_user_movies(user_id)
        movie_info = get_movie_data(title)
        if len(movie_info) < 3:
            return False
        title = movie_info["Title"]
        for movie in data:
            if title in movie["title"]:
                return True
        return False

    def add_user(self, name):
        data = self.get_all_users()
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        data[f"{user_id}"] = {
            "name": name,
            "movies": []
        }
        updated_info = {
            "users": data
        }
        write_data_to_json_file("movies.json", updated_info)

    def add_movie(self, user_id, title):
        data = self.get_all_users()
        movie_info = get_movie_data(title)
        if "Error" in movie_info:
            return "Not found"
        else:
            movie_id = movie_info["imdbID"]
            movie_name = movie_info["Title"]
            director = movie_info["Director"]
            year = movie_info["Year"]
            poster = movie_info["Poster"]
            link = f"https://www.imdb.com/title/{movie_id}/"
            description = movie_info["Plot"]
            try:
                rating = movie_info["imdbRating"]
                if rating == "N/A":
                    rating = 0
            except ValueError:
                rating = 0
            movie = {
                "id": movie_id,
                "title": movie_name,
                "director": director,
                "year": year,
                "rating": float(rating),
                "poster": poster,
                "link": link,
                "description": description
            }
            data[str(user_id)]["movies"].append(movie)
            updated_info = {
                "users": data
            }
            write_data_to_json_file("movies.json", updated_info)

    def update_movie(self, user_id, movie_id, title, director, year, rating):
        data = self.get_all_users()
        movies = data[str(user_id)]["movies"]
        for index, movie in enumerate(movies):
            if movie["id"] == movie_id:
                movie["title"] = title
                movie["director"] = director
                movie["year"] = year
                movie["rating"] = float(rating)
                data[str(user_id)]["movies"][index] = movie
        updated_info = {
            "users": data
        }
        write_data_to_json_file("movies.json", updated_info)

    def get_all_unique_movies(self):
        all_movies = set()
        users = self.get_all_users()
        for user in users.values():
            for movie in user["movies"]:
                all_movies.add(tuple(movie.items()))
        unique_movies = [dict(movie) for movie in all_movies]
        return unique_movies

    def get_movies_paginated(self, page_num, items_per_page=10):
        # Return a list of movies with pagination
        all_movies = self.get_all_unique_movies()
        total_movies = len(all_movies)
        start_idx = (page_num - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_movies)
        return all_movies[start_idx:end_idx]

    def register_user(self, username, password):
        data = self.get_all_users()
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        hashed_password = self.hash_password(password)
        data[f"{user_id}"] = {
            "name": username,
            "password": hashed_password,
            "movies": []
        }
        updated_info = {
            "users": data
        }
        write_data_to_json_file("movies.json", updated_info)
        return user_id

    def check_user(self, name, password):
        data = self.get_all_users()
        for user_data in data.values():
            if user_data["name"] == name and self.check_password(password, user_data["password"]):
                return True
        return False

    def get_id(self, name):
        data = self.get_all_users()
        for user_id, user_data in data.items():
            if user_data["name"] == name:
                return user_id
        return False

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def check_password(self, submitted_password, stored_hashed_password):
        return bcrypt.checkpw(submitted_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))

    def delete_user(self, user_id):
        data = self.get_all_users()
        del data[user_id]
        updated_info = {
            "users": data
        }
        write_data_to_json_file("movies.json", updated_info)

    def update_profile(self, username, photo, upd_name='', upd_surname='', upd_email='', upd_password=''):
        data = self.get_all_users()
        user_id = self.get_id(username)

        if not upd_password:
            hashed_password = data[user_id]['password']
        else:
            hashed_password = self.hash_password(upd_password)
        try:
            data[f"{user_id}"] = {
                "name": username,
                "username": upd_name,
                "surname": upd_surname,
                "email": upd_email,
                "password": hashed_password,
                "photo": photo,
                "movies": data[user_id]["movies"]
            }
        except ValueError:
            pass
        updated_info = {
            "users": data
        }
        write_data_to_json_file("movies.json", updated_info)

    def get_user_info(self, username):
        user_id = self.get_id(username)
        data = self.get_all_users()
        user_info = data[user_id]
        return user_info
