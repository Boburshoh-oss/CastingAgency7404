import os
from flask import (
    Flask,
    request,
    jsonify,
    abort
)
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, setup_db, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    # routes
    ''' sample route '''
    @app.route('/')
    def index():
        return jsonify({
            "success": True,
            "message": "Hello, World!"
        })

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            })
        except:
            abort(422)

    # POST /movies create a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(self):
        body = request.get_json()
        new_title = body.get('title', None)

        new_release_date = body.get('release_date', None)

        if ((new_title is None) or (new_release_date is None)):
            abort(400)
        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.id
            }), 200

        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

        # PATCH /movies/<id> update a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(self, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)
        body = request.get_json()
        new_title = body.get('title')
        new_release_date = body.get('release_date')

        try:
            if new_title:
                movie.title = new_title
            if new_release_date:
                movie.release_date = new_release_date

            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'message':
                f'movie id {movie.id}, titled {movie.title} was deleted',
            })
        except Exception:
            db.session.rollback()
            abort(500)

    # Actors
    @app.route('/actors', methods=["GET"])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.get_formatted_json() for actor in actors],
        }), 200
    # Actors Post

    @app.route('/actors', methods=['POST'])
    @requires_auth("create:actors")
    def add_actor(jwt):
        body = request.get_json()
        name = body.get("name", '')
        age = body.get("age", '')
        gender = body.get("gender", '')
        new_actor = Actor(name=name, gender=gender, age=age)
        if (new_actor.name == '') or \
            (new_actor.age == '') or \
                (new_actor.gender == ''):
            abort(400)
        try:
            new_actor.insert()
            return jsonify({
                "success": True,
                "actor": new_actor.get_formatted_json()}), 201
        except Exception:
            abort(422)

    # Actors Patch
        # PATCH /actors/<id> update an actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(self, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
        body = request.get_json()
        new_age = body.get('age', None)
        new_name = body.get('name', None)
        new_gender = body.get('gender', None)

        if ((new_name is None) and (new_age is None) and (new_gender is None)):
            abort(400)
        try:
            if new_name is not None:
                actor.name = new_name
            if new_age is not None:
                actor.age = new_age
            if new_gender is not None:
                actor.gender = new_gender

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.get_formatted_json()
            }), 200

        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # DELETE ACTORS
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).first()
        if not actor:
            abort(404)

        try:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': actor_id
            }), 200
        except Exception:
            abort(422)

# Error Handling

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(403)
    def foribdden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Foribdden"
        }), 403

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": """Unprocessable Entity.
            An error occured while processing your request"""
        }), 422

    @app.errorhandler(401)
    def unauthorized(e):
        return {
            "success": False,
            "error_code": 401,
            "error_message": "Unauthorized"
        }, 401
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
