import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
import json
import psycopg2
from models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth
sys.path.append(os.getcwd())

db = SQLAlchemy()
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, True')
    response.headers.add('Acess-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
    return response

  @app.route('/actors')
  @requires_auth('get:actors')
  def Get_Actors(payload):
    actors = Actor.query.all()
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
      'success':True,
      'actors':formatted_actors
    }), 200

  @app.route('/movies')
  @requires_auth('get:movies')
  def Get_Movies(payload):
    movies = Movie.query.all()
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
      'success':True,
      'movies':formatted_movies
    }), 200

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def Delete_Actors(payload,actor_id):
    try:
      actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
      if actor is None:
        abort(404)
      actor.delete()
      return jsonify({
        'success':True,
        'deleted':actor_id
      })

    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def Delete_Movies(payload,movie_id):
    try:
      movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
      if movie is None:
        abort(404)
      movie.delete()
      return jsonify({
        'success':True,
        'deleted':movie_id
      }), 200

    except:
      abort(422)
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def Post_Actor(payload):
    body = request.get_json()

    new_name = body.get('name',None)
    new_age = body.get('age', None)
    new_gender = body.get('gender',None)

    if ((new_name is None) or (new_age is None) or (new_gender is None)):
      abort(400)

    Actors = Actor(new_name,new_age,new_gender)
    Actors.insert()
    actors = Actor.query.all()
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
      'success':True,
      'actors':formatted_actors
    }), 200

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def Post_Movie(payload):
    
    body = request.get_json()

    new_title = body.get('title',None)
    new_release_date = body.get('release_date', None)
    new_actor_id = body.get('movie_id',None)
    if ((new_title is None) or (new_release_date is None) or (new_actor_id is None)):
      abort(400)

    Movies = Movie(new_title, new_release_date, new_actor_id)
    Movies.insert()
    movies = Movie.query.all()
    formatted_movies = [movie.format() for movie in movies]

    return jsonify({
      'success':True,
      'movies':formatted_movies
    }),200

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def Patch_Actors(payload,actor_id):
    body = request.get_json()

    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if actor is None:
        abort(404)

      if 'name' in body:
        actor.name = body.get('name')

      if 'age' in body:
        actor.age = body.get('age')

      if 'gender' in body:
        actor.gender = body.get('gender')
      
      actor.update()
      actors = Actor.query.order_by(Actor.id).all()
      formatted_actors = [a.format() for a in actors]
      return jsonify({
        'success':True,
        'actors':formatted_actors
      }), 200

    except:
      abort(404)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def Patch_Movies(payload, movie_id):
    body = request.get_json()
    try:
      movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
      if movie is None:
        abort(404)
      
      if 'title' in body:
        movie.title = body.get('title')
      
      if 'release_date' in body:
        movie.release_date = body.get('release_date')

      if 'movie_id' in body:
        movie.movie_id = body.get('movie_id')
      movie.update()
      movies = Movie.query.order_by(Movie.id).all()
      formatted_movies = [m.format() for m in movies]
      return jsonify({
          'success':True,
          'movies':formatted_movies
      }), 200

    except:
      abort(404)
  
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
      "success":False,
      "error":422,
      "message":"unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success":False,
      "error":400,
      "message":"bad request"
    }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success":False,
      "error":405,
      "message":"method not allowed"
    }), 405
  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
      "success":False,
      "error":401,
      "message":"unauthorized"
    }), 401

  @app.errorhandler(403)
  def forbidden(error):
    return jsonify({
      "success":False,
      "error":403,
      "message":"forbidden"
    }), 403 
  
  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        "success":False,
        "error":error.status_code,
        "message":error.error
    }), error.status_code 
  return app

APP = create_app()
'''
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
'''    