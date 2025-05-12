from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import your models here (User, Planet, Character, favorite_planets, favorite_characters)
# Assuming your models are already declared as provided earlier

# ---------- PEOPLE ----------
@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(person.serialize()), 200

# ---------- PLANETS ----------
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# ---------- USERS ----------
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# ---------- FAVORITES ----------
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.get(1)  # Assuming user_id = 1
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({
        "favorite_planets": [planet.serialize() for planet in user.favorite_planets],
        "favorite_characters": [character.serialize() for character in user.favorite_characters]
    }), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.get(1)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({"msg": "User or Planet not found"}), 404
    if planet not in user.favorite_planets:
        user.favorite_planets.append(planet)
        db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user = User.query.get(1)
    character = Character.query.get(people_id)
    if not user or not character:
        return jsonify({"msg": "User or Character not found"}), 404
    if character not in user.favorite_characters:
        user.favorite_characters.append(character)
        db.session.commit()
    return jsonify({"msg": "Character added to favorites"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user = User.query.get(1)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({"msg": "User or Planet not found"}), 404
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
    return jsonify({"msg": "Planet removed from favorites"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_person(people_id):
    user = User.query.get(1)
    character = Character.query.get(people_id)
    if not user or not character:
        return jsonify({"msg": "User or Character not found"}), 404
    if character in user.favorite_characters:
        user.favorite_characters.remove(character)
        db.session.commit()
    return jsonify({"msg": "Character removed from favorites"}), 200

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)
