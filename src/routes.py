"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import request, jsonify, Blueprint
from models import db, Character
from utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)  


@api.route('/hello', methods=['GET', 'POST'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message from the backend. Check your network tab!"
    }
    return jsonify(response_body), 200


@api.route("/character", methods=['GET'])
def handle_character():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200


@api.route("/create-character", methods=['POST'])
def handle_create_character():
    data = request.get_json()

    name = data.get("name")
    height = data.get("height")
    hair_color = data.get("hair_color")
    eye_color = data.get("eye_color")
    gender = data.get("gender")

    
    if not all([name, height, hair_color, eye_color, gender]):
        return jsonify({"msg": "Some fields are missing in your request"}), 400

    
    existing = Character.query.filter_by(name=name).first()
    if existing:
        return jsonify({"msg": "A character with this name already exists"}), 409

    
    new_character = Character(
        name=name,
        height=height,
        hair_color=hair_color,
        eye_color=eye_color,
        gender=gender
    )
    db.session.add(new_character)
    db.session.commit()
    db.session.refresh(new_character)

    return jsonify({
        "msg": "Character successfully created!",
        "character": new_character.serialize()
    }), 201
