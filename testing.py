import json
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
