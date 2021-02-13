import os
from flask import Flask, request, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Movie, Actor
from auth import AuthError, requires_auth

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_BASE_URL = 'https://' + os.environ['AUTH0_DOMAIN']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']
AUTH0_API_AUDIENCE = os.environ['AUTH0_API_AUDIENCE']


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    moment = Moment(app)
    app.secret_key = "mysecretkey"
    setup_db(app)

    '''
    Set up CORS(Cross Origin Resource Sharing).
    Allow '*' for all origins.
    Delete the sample route after implementing the API endpoints
    '''
    CORS(app, resources={"/": {"origin": "*"}})

    '''
    CORS Headers. Use the after_request decorator
    to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Casting Agency',
        })

    # Movie Routes
    '''
    @Implement endpoint
    GET /movies
        it should require the 'get:movies' permission
    returns status code 200 and json {"success": True, "movies": movies}
        where movies is the list of movies
        or appropriate status code indicating reason for failure
    '''

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:
            movies = Movie.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.format for movie in movies]
            }), 200
        except BaseException:
            abort(404)

    '''
    @Implement endpoint
    GET /movies/<id>
        where <id> is the existing movie id
        it should require the 'get:movies' permission
        it should respond with a 404 error if <id> is not found
    returns status code 200 and json {"success": True, "movie": movie}
        where movie is the movie with specific id
        or appropriate status code indicating reason for failure
    '''

    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_by_specific_id(jwt, id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format(),
            }), 200

    '''
    @Implement endpoint
    POST /movies
        it should create a new row in the movie table
        it should require the 'post:movies' permission
    returns status code 200 and json {"success": True, "movie": movie}
        where movie is an array containing only the newly created movie
        or appropriate status code indicating reason for failure
    '''

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        body = request.get_json()

        if not('title' in body and 'release_date' in body):
            abort(422)

        title = body.get('title')
        release_date = body .get('release_date')

        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format,
            })
        except BaseException:
            abort(422)

    '''
    @Implement endpoint
    PATCH /movies/<id>
        where <id> is the existing movie id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:movies' permission
    returns status code 200 and json {"success": True, "movie": movie}
        where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
    '''

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        movie = Movie.query.get(id)
        if movie:
            try:
                body = request.get_json()

                title = body.get('title')
                if title:
                    movie .title = title

                release_date = body.get('release_date')
                if release_date:
                    movie.release_date = release_date

                movie.update()
                return jsonify({
                    'success': True,
                    'movie': [movie.format()],
                })

            except BaseException:
                abort(422)
        else:
            abort(404)

    '''
    @Implement endpoint
    DELETE /movies/<id>
        where <id> is the existing movie id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:movies' permission
    returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    '''

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie:
            try:
                movie.delete()
                return jsonify({
                    'success': True,
                    'delete': id,
                })
            except BaseException:
                abort(422)
        else:
            abort(404)

    # Actor Routes
    '''
    @Implement endpoint
    GET /actors
        it should require the 'get:actors' permission
    returns status code 200 and json {"success": True, "actors": actors}
        where actors is the list of actors
        or appropriate status code indicating reason for failure
    '''

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        try:
            actors = Actor.query.all()
            return jsonify({
                'success': True,
                'actors': [actor.format for actor in actors]
            }), 200
        except BaseException:
            abort(404)

    '''
    @Implement endpoint
    GET /actors/<id>
        where <id> is the existing actor id
        it should require the 'get:actors' permission
        it should respond with a 404 error if <id> is not found
    returns status code 200 and json {"success": True, "actor": actor}
        where actor is the actor with specific id
        or appropriate status code indicating reason for failure
    '''

    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_by_specific_id(jwt, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 200

    '''
    @Implement endpoint
    POST /actors
        it should create a new row in the actor table
        it should require the 'post:actors' permission
    returns status code 200 and json {"success": True, "actor": actor}
        where actor is an array containing only the newly created actor
        or appropriate status code indicating reason for failure
    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        body = request.get_json()

        if not('name' in body and 'gender' in body and 'age' in body):
            abort(422)

        name = body.get('name')
        gender = body .get('gender')
        age = body .get('age')

        try:
            actor = Actor(name=name, gender=gender, age=age)
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format,
            })
        except BaseException:
            abort(422)

    '''
    @Implement endpoint
    PATCH /actors/<id>
        where <id> is the existing actor id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:actors' permission
    returns status code 200 and json {"success": True, "actor": actor}
        where movie an array containing only the updated actor
        or appropriate status code indicating reason for failure
    '''

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        actor = Actor.query.get(id)
        if actor:
            try:
                body = request.get_json()

                name = body.get('name')
                if name:
                    actor.name = name

                gender = body.get('gender')
                if gender:
                    actor.gender = gender

                age = body.get('age')
                if age:
                    actor.age = age

                actor.update()
                return jsonify({
                    'success': True,
                    'actor': [actor.format()],
                })

            except BaseException:
                abort(422)
        else:
            abort(404)

    '''
    @Implement delete endpoint
    DELETE /actors/<id>
        where <id> is the existing actor id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:actors' permission
    returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    '''

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'delete': id,
                })
            except BaseException:
                abort(422)
        else:
            abort(404)

    # Error Handling

    '''
    Create error handlers for all expected errors
    including 400, 404, 422 and 500.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    '''
    Implement error handler for AuthError
    '''

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        return jsonify({
            "success": False,
            "error": exception.status_code,
            "message": exception.error,
        }), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
