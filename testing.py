import json
import requests

API_KEY = "1b44b07a"


def get_movie_data(title):
    try:
        api_url = f'https://www.omdbapi.com/?t={title}&apikey={API_KEY}'
        response = requests.get(api_url)
        text_response = response.text
        json_response = json.loads(text_response)
        return json_response
    except requests.RequestException:
        return {"Error": "No internet"}


def get_all_users():
    # Return all the users all users
    with open("movies.json") as file:
        data = json.load(file)
        users = data["users"]
    return users


def list_all_users():
    users_data = get_all_users()
    users_list = []
    for user_id, user in users_data.items():
        users = {
            "id": user_id,
            "name": user["name"]
        }
        users_list.append(users)
    return users_list


print(list_all_users())
print(get_movie_data("Iron"))
