from os import getenv
from sqlalchemy import Column, String, Integer, create_engine, Date
from flask_sqlalchemy import SQLAlchemy
import json
from config import database_param
from os import getenv




database_path=getenv("DATABASE_URI")


# database_path = "{}://{}:{}@localhost: 5432/{}".format(
#                                    database_param["dialect"],
#                                    database_param["username"],
#                                    database_param["password"],
#                                    database_param["db_name"])

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(Date, nullable=False)
    actors = db.relationship('Actor', cascade="all, delete",backref='movies')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.name for actor in self.actors]}

class Actor(db.Model):
    __tablename__ = 'Actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_formatted_json(self):
        return({
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        })

    def repr(self):
        return f'Actor: {self.id}, {self.name}'