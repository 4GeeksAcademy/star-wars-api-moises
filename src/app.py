"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, FavoritePeople, FavoritePlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify(person.serialize())
    return jsonify({"error": "Person not found"}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize())
    return jsonify({"error": "Planet not found"}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        favorites = {
            "people": [person.serialize() for person in user.favorites_people],
            "planets": [planet.serialize() for planet in user.favorites_planets]
        }
        return jsonify(favorites)
    return jsonify({"error": "User not found"}), 404

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if user and planet:
        favorite = FavoritePlanets(user_id=user.id, planet_id=planet.id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"msg": "Planet added to favorites"})
    return jsonify({"error": "User or Planet not found"}), 404

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    person = People.query.get(people_id)
    if user and person:
        favorite = FavoritePeople(user_id=user.id, people_id=person.id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"msg": "People added to favorites"})
    return jsonify({"error": "User or People not found"}), 404

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if user and planet:
        favorite = FavoritePlanets.query.filter_by(user_id=user.id, planet_id=planet.id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"msg": "Planet removed from favorites"})
    return jsonify({"error": "User or Planet not found"}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    person = People.query.get(people_id)
    if user and person:
        favorite = FavoritePeople.query.filter_by(user_id=user.id, people_id=person.id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"msg": "People removed from favorites"})
    return jsonify({"error": "User or People not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)