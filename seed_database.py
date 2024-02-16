""""Create database"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
with server.app.app_context():
    model.db.create_all()

# # populate movies from JSON
with open("data/movies.json") as f:
    movie_data = json.loads(f.read())


movie_db = []
with server.app.app_context():
# #store movies in a list
    for movie in movie_data:
        title, overview, poster_path = (
            movie["title"],
            movie["overview"],
            movie["poster_path"]
        )
        release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

        db_movie = crud.create_movie(title, overview, release_date, poster_path)
        movie_db.append(db_movie)
    model.db.session.add_all(movie_db)
    model.db.session.commit()



    for n in range(10):
        email = f"user{n}@test.com"
        password = "test"

        user = crud.create_user(email, password)
        model.db.session.add(user)


        for _ in range(10):
            random_movie = choice(movie_db)
            score = randint(1, 5)

            rating = crud.create_rating(user, random_movie, score)

            model.db.session.add(rating)

    model.db.session.commit()

# if __name__ == "__main__":
