from flask import Flask, request, render_template, jsonify, redirect
from datamanager.json_data_manager_interface import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file


@app.route('/')
def home():
    return render_template('home_page.html'), 200


@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>', methods=['GET'])
def list_user_movie(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_id=user_id, movies=movies)


@app.route("/add_user", methods=["GET", "POST"])
def add_new_user():
    if request.method == "POST":
        name = request.form.get("name")
        if data_manager.user_exist(name):
            return jsonify("User already exist, choose another user name!")
        else:
            data_manager.add_user(name)
            return redirect("/users")
    return render_template("add_user.html")


@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_new_movie(user_id):
    if request.method == "POST":
        title = request.form.get("title")
        if data_manager.movie_exist(title, user_id):
            return jsonify("Movie already added")

        result = data_manager.add_movie(user_id, title)
        if result == "Not found":
            return jsonify("Movie not found")

        # Redirect to the user's movie page
        return redirect(f"/users/{user_id}")
    return render_template("add_movie.html", user_id=user_id, back_url=f"/users/{user_id}")


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    movie = data_manager.get_movie(user_id, movie_id)
    if request.method == "POST":
        # Get the updated data from the form
        updated_title = request.form.get("title")
        updated_director = request.form.get("director")
        updated_year = request.form.get("year")
        updated_rating = request.form.get("rating")

        # Update the movie with the new data
        data_manager.update_movie(user_id, movie_id, updated_title, updated_director, updated_year, updated_rating)

        # Redirect to the user's movie page
        return redirect(f"/users/{user_id}")
    return render_template("update_movie.html", user_id=user_id, movie_id=movie_id, movie=movie)


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["GET"])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(f"/users/{user_id}")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
