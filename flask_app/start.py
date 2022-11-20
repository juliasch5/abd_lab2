from app import app
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from app.database.database import db
from datetime import datetime
import pandas as pd
import random

class Media(db.Model):
    __tablename__ = "Media"
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(128), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    language = db.Column(db.String(128), unique=False, nullable=False)
    localization = db.Column(db.String(128), unique=False, nullable=False)

class Genre(db.Model):
    __tablename__ = "Genre"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(
        self,
        name,
    ):
        self.name = name

genre_table = db.Table('genre_table',
                    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id')),
                    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'))
                    )

class Movie(Media):
    __tablename__ = "Movie"
    members = relationship("Role", lazy="select")
    genres = relationship("Genre", secondary=genre_table, backref="Movies")
    def __init__(
        self,
        title,
        year,
        language,
        localization,
    ):
        self.title = title
        self.year = year
        self.language = language
        self.localization = localization

class Series(Media):
    __tablename__ = "Serie"
    start_date = db.Column(db.DateTime, unique=False, nullable=False)
    end_date = db.Column(db.DateTime, unique=False, nullable=True)
    seasons = relationship('Season', lazy='select')

    def __init__(
        self,
        title,
        year,
        language,
        localization,
        start_date,
        end_date
    ):
        self.title = title
        self.year = year
        self.language = language
        self.localization = localization
        self.start_date = start_date
        self.end_date = end_date
 
class Episode(Movie):
    __tablename__ = "Episode"
    episode_number = db.Column(db.Integer, unique=False, nullable=True)
    season_id = db.Column(db.Integer, db.ForeignKey('Season.id'), nullable=True)

    def __init__(
        self,
        title,
        year,
        language,
        localization,
        episode_number,
        season_id
    ):
        self.title = title
        self.year = year
        self.language = language
        self.localization = localization
        self.episode_number = episode_number
        self.season_id = season_id

class Season(db.Model):
    __tablename__ = "Season"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    season_number = db.Column(db.Integer, unique=False, nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey('Serie.id'))
    episodes = relationship('Episode', lazy='select')

    def __init__(
        self,
        season_number,
        series_id,
    ):
        self.season_number = season_number
        self.series_id = series_id

class Role(db.Model):
    __tablename__ = "Role"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    surname = db.Column(db.String(128), unique=False, nullable=False)
    role_name = db.Column(db.String(128), unique=False, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'))

    def __init__(
        self,
        name,
        surname,
        role_name,
        movie_id
    ):
        self.name = name
        self.surname = surname
        self.role_name = role_name
        self.movie_id = movie_id



def load_data_from_csv():
    genres_csv = pd.read_csv(r"./sample_data/Genres.csv", delimiter=",")
    global genres_df
    genres_df = pd.DataFrame(
        genres_csv,
        columns=["name",],
    )

    global geners
    geners = []
    for index, row in genres_df.iterrows():
        geners.append(Genre(name=row['name']))

    movies_csv = pd.read_csv(r"./sample_data/Movies.csv", delimiter=",")
    global movies_df
    movies_df = pd.DataFrame(
        movies_csv,
        columns=['title', 'year', 'language', 'localization',],
    )

    series_csv = pd.read_csv(r"./sample_data/Series.csv", delimiter=",")
    global series_df
    series_df = pd.DataFrame(
        series_csv,
        columns=['title', 'year', 'language', 'localization', 'start_date', 'end_date',]
    )

    seasons_csv = pd.read_csv(r"./sample_data/Seasons.csv", delimiter=",")
    global seasons_df
    seasons_df = pd.DataFrame(
        seasons_csv,
        columns=['season_number', 'series_id',],
    )

    episodes_csv = pd.read_csv(r"./sample_data/Episodes.csv", delimiter=",")
    global episodes_df
    episodes_df = pd.DataFrame(
        episodes_csv,
        columns=['title', 'year', 'language', 'localization', 'episode_number', 'season_id',],
    )

    roles_csv = pd.read_csv(r"./sample_data/Roles.csv", delimiter=",")
    global roles_df
    roles_df = pd.DataFrame(
        roles_csv,
        columns=['name', 'surname', 'role_name', 'movie_id',],
    )

    print(movies_df)
    print(series_df)
    print(seasons_df)
    print(episodes_df)
    print(roles_df)

    print("loaded data from csv")


def create_db_schema():
    with app.app_context():
        db.drop_all()
    with app.app_context():
        db.create_all()
        db.session.commit()


def load_movies_to_database_from_global_df():
    with app.app_context():
        for index, row in movies_df.iterrows():
            movie = Movie(
                title=row["title"],
                year=row["year"],
                language=row["language"],
                localization=row["localization"],
            )
            movie.genres.append(random.choice(geners))
            if index % 4 == 0:
                movie.genres.append(random.choice(geners))
            if index % 5 == 0:
                movie.genres.append(random.choice(geners))
            db.session.add(movie)
        db.session.commit()
    print("loaded movies to database")


def load_series_to_database_from_global_df():
    with app.app_context():
        for index, row in series_df.iterrows():
            series = Series(
                title=row["title"],
                year=row["year"],
                language=row["language"],
                localization=row["localization"],
                start_date=row["start_date"],
                end_date=row["end_date"],
            )
            db.session.add(series)
        db.session.commit()
    print("loaded series to database")


def load_seasons_to_database_from_global_df():
    with app.app_context():
        for index, row in seasons_df.iterrows():
            season = Season(
                season_number=int(float(row["season_number"])),
                series_id=int(float(row["series_id"])),
            )
            db.session.add(season)
        db.session.commit()
    print("loaded seasons to database")


def load_episodes_to_database_from_global_df():
    with app.app_context():
        for index, row in episodes_df.iterrows():
            episode = Episode(
                title=row["title"],
                year=row["year"],
                language=row["language"],
                localization=row["localization"],
                episode_number=int(float(row["episode_number"])),
                season_id=int(float(row["season_id"])),
            )
            episode.genres.append(random.choice(geners))
            if index % 4 == 0:
                episode.genres.append(random.choice(geners))
            if index % 5 == 0:
                episode.genres.append(random.choice(geners))
            db.session.add(episode)
        db.session.commit()
    print("loaded episodes to database")


def load_roles_to_database_from_global_df():
    with app.app_context():
        for index, row in roles_df.iterrows():
            role = Role(
                name=row["name"],
                surname=row["surname"],
                role_name=row["role_name"],
                movie_id=int(float(row["movie_id"])),
            )
            db.session.add(role)
        db.session.commit()
    print("loaded roles to database")


def setup_database_and_load_small_data():

    with app.app_context():

        genre1 = Genre(
                name="comedy"
            )

        genre2 = Genre(
                name="thriller"
            )

        movie1 = Movie(
                title="Parasite",
                year="2019",
                language="korean",
                localization="South Korea",
            )

        movie1.genres.append(genre1)
        movie1.genres.append(genre2)
        db.session.add(movie1)
        db.session.commit()

        role1 = Role(
                name="Kang-ho",
                surname="Song",
                role_name="main character",
                movie_id=movie1.id,
            )
        db.session.add(role1)
        db.session.commit()

        series1 = Series(
                title="Friends",
                year="1994",
                language="english",
                localization="United States",
                start_date=datetime.strptime("Sep 22 1994", "%b %d %Y"),
                end_date=datetime.strptime("May 6 2004", "%b %d %Y"),
            )
        db.session.add(series1)
        db.session.commit()

        season1 = Season(
                season_number=2,
                series_id=series1.id,
            )
        db.session.add(season1)
        db.session.commit()

        episode1 = Episode(
                title="The One with the Prom Video",
                year="1996",
                language="english",
                localization="United States",
                episode_number=14,
                season_id=season1.id,
            )

        episode1.genres.append(genre1)
        print(episode1)
        db.session.add(episode1)
        db.session.commit()



app = Flask(__name__, template_folder="app/templates")
app.config.from_object("app.config.Config")
app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)
migrate = Migrate(app, db)
create_db_schema()
# setup_database_and_load_small_data()
load_data_from_csv()
load_movies_to_database_from_global_df()
load_series_to_database_from_global_df()
load_seasons_to_database_from_global_df()
load_episodes_to_database_from_global_df()
load_roles_to_database_from_global_df()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


# def configure_dependencies(binder):
#     binder.bind(SQLAlchemy, to=db, scope=flask_injector.singleton)

# flask_injector.FlaskInjector(app=app, modules=[configure_dependencies])
# print("DONE")
