import json
from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return all the users all users
        with open(self.filename) as file:
            data = json.load(file)
            users = data["users"]
        return users

    def get_user_movies(self, user_id):
        # Return all the movies for a given user
        users = self.get_all_users()
        user_movies = None
        for id_of_user, user in users.items():
            if id_of_user == user_id:
                user_movies = user["movies"]
        return user_movies

    def list_all_users(self):
        users_data = self.get_all_users()
        users_list = []
        for user_id, user in users_data.items():
            users = {
                "id": user_id,
                "name": user["name"]
            }
            users_list.append(users)
        return users_list

    def get_movie(self, user_id, movie_id):
        data = self.get_user_movies(user_id)
        for movie in data:
            if movie["id"] == movie_id:
                return movie

    def delete_movie(self, user_id, movie_id):
        data = self.get_user_movies(user_id)
        for movie in data:
            if movie["id"] == movie_id:
                del movie
