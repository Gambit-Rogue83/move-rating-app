"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/users")
def all_users():

    users = crud.get_users()
    return render_template("all_users.html", users =users)

@app.route("/users", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("That email is already connected to an existing account. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account Created. Please, Log in")

    return redirect("/")


@app.route("/users/<user_id>")
def user_profile(user_id):

    user = crud.get_profile(user_id)
    return render_template("user_profile.html", user =user)

@app.route("/login", methods=["POST"])
def log_in():

    email = request.form.get("email")
    password = request.form.get("password")


    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("You've entered invalid data. Try again")
    else:
        session["user_email"] = user.email
        flash(f"{user.email} access granted!")

    return redirect("/")

@app.route("/movies")
def all_movies():

    movies = crud.display_all_movies()
    return render_template("all_movies.html", movies =movies)

@app.route("/movies/<movie_id>")
def movie_details(movie_id):

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie =movie)

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):

    logged_in = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in is None:
        flash("You must log in first")
    elif not rating_score:
        flash("You must enter a rating first")
    else:
        user = crud.get_user_by_email(logged_in)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"Thanks for rating {movie.title}")

    return redirect(f"/movies/{movie_id}")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
