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
from models import db, User, Character, Planet, Favorite  

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    return jsonify({'data': users_serialized}), 200


@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    people_serialized = []
    for person in people:
        people_serialized.append(person.serialize())
    return jsonify({'data': people_serialized}), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = Character.query.get(people_id)
    if person is None:
        return jsonify({'msg': 'Character not found'}), 404
    return jsonify({'data': person.serialize()}), 200



@app.route('/people', methods=['POST'])
def add_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'debes enviar informacion en el body'}), 400

    if 'name' not in body:
        return jsonify({'msg': 'el campo name es obligatorio'}), 400
    if 'height' not in body:
        return jsonify({'msg': 'el campo height es obligatorio'}), 400
    if 'description' not in body:
        return jsonify({'msg': 'el campo description es obligatorio'}), 400

    new_character = Character()
    new_character.name = body['name']
    new_character.height = body['height']
    new_character.description = body['description'] 
    # planet_id es opcional
    if 'planet_id' in body:
        new_character.planet_id = body['planet_id']

    db.session.add(new_character)
    db.session.commit()

    return jsonify({'msg': 'Character agregado', 'data': new_character.serialize()}), 201



@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())
    return jsonify({'data': planets_serialized}), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}), 404
    return jsonify({'data': planet.serialize()}), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorites_serialized = []
    for fav in favorites:
        favorites_serialized.append(fav.serialize())

    return jsonify({'data': favorites_serialized}), 200


@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404

    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}), 404

    existing_fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_fav is not None:
        return jsonify({'msg': 'Favorite already exists'}), 409

    new_fav = Favorite()
    new_fav.user_id = user_id
    new_fav.planet_id = planet_id

    db.session.add(new_fav)
    db.session.commit()

    return jsonify({'msg': 'Favorite planet added', 'data': new_fav.serialize()}), 201


@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_people(people_id, user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404

    person = Character.query.get(people_id)
    if person is None:
        return jsonify({'msg': 'Character not found'}), 404

    existing_fav = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if existing_fav is not None:
        return jsonify({'msg': 'Favorite already exists'}), 409

    new_fav = Favorite()
    new_fav.user_id = user_id
    new_fav.character_id = people_id

    db.session.add(new_fav)
    db.session.commit()

    return jsonify({'msg': 'Favorite people added', 'data': new_fav.serialize()}), 201


@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):
    fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if fav is None:
        return jsonify({'msg': 'Favorite not found'}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({'msg': 'Favorite planet deleted'}), 200


@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_people(people_id, user_id):
    fav = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if fav is None:
        return jsonify({'msg': 'Favorite not found'}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({'msg': 'Favorite people deleted'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
