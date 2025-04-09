"""
This module starts the API server, loads the DB, and defines endpoints.
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import (db, Planet, Character, User, favorite_characters, favorite_planets)

from sqlalchemy import delete

app = Flask(__name__)
app.url_map.strict_slashes = False

# Database configuration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize plugins
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors as JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap with all endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Sample user endpoint
@app.route('/user', methods=['GET'])
def handle_hello():

        response_body = {
            "msg: Hello, this is your GET/user response"
        }
        return jsonify(response_body), 200

@app.route('/users', methods=["GET"])
def get_all_users():
    users = User.query.all()
    serialized_users = []
    for character in users:
        serialized_users.append(character.serialize())
    ## ALternative way to do the same thing = the above 3 lines
    # List comprehension:
    # serilized_users = [character.serialise() for character in users]
    # Map function:
    # serialized_users = list(map(lambda character: character.serialize(), users))

    response_body = {
        "msg": "Here is your list of users", "users": serialized_users
    }

    return jsonify(serialized_users), 200
   
@app.route('/users/favorites', methods=['GET'])
def get_current_favs():
     user = User.query.filter_by(username="Test user").first()
     if not user:
          db.session.merge(User(
               username="Test user",
               password="test"
          ))
          db.session.commit()
          return jsonify(
               favorite_planets=[
                    planet.serialize() for planet in user.favorite_planets
               ],
          )
         
@app.route("/favorite/planet/'<int:planet_id>",methods=["POST"])
def add_favorite_planets(planet_id:int):
     user= User.query.filter_by(username="Test user").first()
     if not user:
         return jsonify(msg="User doesn't exist."), 404
     planet= Planet.query.filter_by(id=planet_id).first()
     user.favorite_planets.append(planet)
     db.session.merge(user)
     db.session.commit()
     db.session.refresh(user)
     return jsonify(favorite_planets=[
         planet.serialize() for planet in user.favorite_planets
     ])

     # [DELETE] /favorite/planet/<int:planet_id> Delete a favorite planet with the id = planet_id.
@app.route("/favorite/planet/<int:planet_id>",methods=["DELETE"])
def remove_favorite_planets(planet_id:int):
    user= User.query.filter_by(username="Test user").first()
    if not user:
         return jsonify(msg="User doesn't exist."), 404
    user.favorite_planets=list(filter(
        lambda planet: planet.id != planet_id,
        user.favorite_planets
    ))

    db.session.merge(user)
    db.session.commit()
    db.session.refresh(user)
    return jsonify(favorite_planets=[
         planet.serialize() for planet in user.favorite_planets
])
     
     # [POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.
@app.route("/favorite/chars/<int:char_id>",methods=["POST"])
def add_fav_char(char_id:int):
    user= User.query.filter_by(username="Test user").first()
    if not user:
         return jsonify(msg="User doesn't exist."), 404
    char= Character.query.filter_by(id=char_id).first()
    user.favorite_characters.append(char)
    db.session.merge(user)
    db.session.commit()
     

# Main app execution
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
