from flask import Flask, request, render_template, jsonify
from datamanager.json_data_manager_interface import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>', methods=['GET'])
def list_user_movie(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_id=user_id, movies=movies)


@app.route("/add_user", methods=["POST"])
def add_new_user():
    pass


@app.route("/users/<user_id>/add_movie", methods=["POST"])
def add_new_movie(user_id):
    pass


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["PUT"])
def update_movie(user_id, movie_id):
    movie = data_manager.get_movie(user_id, movie_id)
    pass


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["DELETE"])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return jsonify("Movie deleted successfully!"), 200


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Ups ss! Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Ups sess! Method Not Allowed"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
