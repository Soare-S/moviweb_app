import os
from flask import Flask, request, render_template, redirect, session
from werkzeug.utils import secure_filename
from configuration.key import SECRET_KEY
from datamanager.json_data_manager_interface import JSONDataManager

app = Flask(__name__)
app.secret_key = SECRET_KEY
data_manager = JSONDataManager('data/movies.json')  # Use the appropriate path to your JSON file


def check_session():
    try:
        user = session['username']
        return user
    except KeyError:
        return False


def paginating_movies():
    # Get all unique movies
    all_unique_movies = data_manager.get_all_unique_movies()

    # Paginate the movies (You can adjust the number of movies per page)
    movies_per_page = 10
    page = int(request.args.get('page', 1))
    start_index = (page - 1) * movies_per_page
    end_index = start_index + movies_per_page
    paginated_movies = all_unique_movies[start_index:end_index]

    # Calculate total number of pages for pagination links
    total_pages = (len(all_unique_movies) + movies_per_page - 1) // movies_per_page
    return page, paginated_movies, total_pages


@app.route('/')
def home():
    # Get all unique movies
    page, paginated_movies, total_pages = paginating_movies()
    current_user = check_session()
    if current_user:
        user_info = data_manager.get_user_info(current_user)
    else:
        user_info = ""
    user_id = data_manager.get_id(current_user)

    return render_template('home_page.html', movies=paginated_movies, total_pages=total_pages, current_page=page,
                           current_user=current_user, user_id=user_id, user_info=user_info)


@app.route('/users')
def list_users():
    current_user = check_session()
    users = data_manager.list_all_users()
    if current_user:
        user_id = data_manager.get_id(current_user)
        session.pop('username', None)
        error_message = "You have been successfully logged out!"
        return render_template('users.html', users=users, user_id=user_id, error_message=error_message)
    else:
        return render_template('users.html', users=users)


@app.route('/users/<user_id>', methods=['GET'])
def list_user_movie(user_id):
    movies = data_manager.get_user_movies(user_id)
    current_user = check_session()
    if current_user:
        user_info = data_manager.get_user_info(current_user)
    else:
        user_info = ""
    return render_template('user_movies.html', user_id=user_id, movies=movies, current_user=current_user, user_info=user_info)


@app.route("/add_user", methods=["GET", "POST"])
def add_new_user():
    if request.method == "POST":
        name = request.form.get("name")
        # Check if the username field is empty
        if not name or len(name) < 3:
            return render_template("add_user.html", error_message="Please enter an username, at least 3 characters.")

        elif data_manager.user_exist(name):
            return render_template("add_user.html",
                                   error_message=f'User {name} already exist, choose another user name!')
        else:
            data_manager.add_user(name)
            return redirect("/users")
    return render_template("add_user.html")


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])
def add_new_movie(user_id):
    current_user = check_session()
    if current_user:
        user_info = data_manager.get_user_info(current_user)
    else:
        user_info = ""
    if request.method == "POST":
        title = request.form.get("title")
        if data_manager.movie_exist(title, user_id):
            return render_template("add_movie.html", user_id=user_id,
                                   error_message=f'Movie already exist!', current_user=current_user)

        result = data_manager.add_movie(user_id, title)
        if result == "Not found":
            return render_template("add_movie.html", user_id=user_id, back_url=f"/users/{user_id}",
                                   error_message=f'Movie not found, try to enter more appropriate name',
                                   current_user=current_user)

        # Redirect to the user's movie page
        return redirect(f"/users/{user_id}")
    return render_template("add_movie.html", user_id=user_id, back_url=f"/users/{user_id}",
                           current_user=current_user, user_info=user_info)


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
    current_user = check_session()
    if current_user:
        user_info = data_manager.get_user_info(current_user)
    else:
        user_info = ""
    return render_template("update_movie.html", user_id=user_id, movie_id=movie_id, movie=movie,
                           current_user=current_user, user_info=user_info)


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["GET"])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(f"/users/{user_id}")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            error_message = "Please enter username and password to register."
            return render_template("register.html", error_message=error_message)
        elif len(username) < 2:
            error_message = "Username must be at least 2 characters."
            return render_template("register.html", error_message=error_message)
        elif data_manager.user_exist(username):
            error_message = f"User: {username} - already exist. Please select another username."
            return render_template("register.html", error_message=error_message)
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters."
            return render_template("register.html", error_message=error_message)
        else:
            session['username'] = username
            current_user = check_session()
            user_id = data_manager.register_user(username, password)
            user_info = data_manager.get_user_info(username)
            message = f"Hi, {username}.\nWelcome to your movieweb app account!"
            empty_message = "At the moment your movie list is empty. Add some movies to get started."
            return render_template("user_account.html", empty_message=empty_message, message=message,
                                   user_id=user_id, current_user=current_user, user_info=user_info), 200
    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        success = data_manager.check_user(username, password)
        if success:
            session['username'] = username
            message = f"Welcome back {username}! Enjoy your movies"
            user_id = data_manager.get_id(username)
            movies = data_manager.get_user_movies(user_id)
            current_user = check_session()
            user_info = data_manager.get_user_info(username)
            return render_template("user_account.html", message=message, movies=movies, user_id=user_id,
                                   current_user=current_user, user_info=user_info)
        else:
            page, paginated_movies, total_pages = paginating_movies()
            user_id = data_manager.get_id(username)
            error_message = "Sorry, wrong password"
            return render_template('home_page.html', movies=paginated_movies, total_pages=total_pages,
                                   current_page=page, user_id=user_id, message=error_message)


@app.route('/delete_user/<user_id>', methods=["GET", "POST"])
def delete_user(user_id):
    current_user = check_session()
    if request.method == "POST":
        password = request.form.get("password")
        if current_user:
            user_id = data_manager.get_id(current_user)
            success = data_manager.check_user(current_user, password)
            if success:
                data_manager.delete_user(user_id)
                session.pop('username', None)
                message = "User deleted successfully!"
            else:
                message = "Sorry wrong password!"
                return render_template('delete_user.html', current_user=current_user, user_id=user_id,
                                       error_message=message)
        else:
            if password == SECRET_KEY:
                data_manager.delete_user(user_id)
                message = "User deleted successfully!"
            else:
                message = "Sorry, wrong secret key."
        users = data_manager.list_all_users()
        return render_template('users.html', error_message=message, users=users)
    else:
        return render_template('delete_user.html', current_user=current_user, user_id=user_id)


@app.route('/user_profile/<username>', methods=['GET', 'POST'])
def user_profile(username):
    current_user = check_session()
    user_info = data_manager.get_user_info(username)
    user_id = data_manager.get_id(username)
    back_url = f"/users/{user_id}"
    if request.method == 'POST':
        # Get the updated data from the form
        updated_name = request.form.get("username")
        updated_surname = request.form.get("surname")
        updated_email = request.form.get("email")
        updated_password = request.form.get("password")
        if 'photo' in request.files:
            # Handle photo upload
            photo = request.files['photo']
            if photo.filename != '':
                photo_filename = secure_filename(photo.filename)
                photo.save(os.path.join('static/upload_folder', photo_filename))
                photo = photo_filename

        if 'delete_photo' in request.form:
            # Handle photo deletion
            photo = ''

        # Update the movie with the new data
        data_manager.update_profile(username, photo, updated_name, updated_surname, updated_email, updated_password)

        # Redirect to the user's movie page
        return redirect(back_url)

    return render_template('user_profile.html', username=username, user_info=user_info, current_user=current_user,
                           back_url=back_url)


@app.route('/logout', methods=["GET"])
def logout():
    session.pop('username', None)
    return render_template('logout.html')


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
