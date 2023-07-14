import csv
from .data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        users = []
        with open('data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
        return users

    def get_user_movies(self, user_id):
        # Return all the movies for a given user
        user_movies = []
        with open('data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == user_id:
                    user_movies.append(row)
        return user_movies
