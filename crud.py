"""CRUD OPERATIONS"""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user"""

    user = User(email =email, password =password)

    return user

def get_user_by_email(email):

    user = User.query.filter(User.email == email).first()
    return user

def get_users():

    return User.query.all()

def get_profile(user_id):

    return User.query.get(user_id)

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie"""

    movie = Movie(
        title =title,
        overview =overview,
        release_date =release_date,
        poster_path =poster_path)

    return movie

def display_all_movies():

    return Movie.query.all()

def get_movie_by_id(movie_id):

    return Movie.query.get(movie_id)

def create_rating(user, movie, score):
    """Create a rating"""

    rating = Rating(
        user_id =user.user_id,
        movie_id =movie.movie_id,
        score =score,
        user =user,
        movie = movie
    )

    return rating

def update_rating(rating_id, new_score):

    rating = Rating.query.get(rating_id)
    rating.score = new_score

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
