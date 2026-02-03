from flask import Blueprint, jsonify, request
from models import db, User, Character, Location

api = Blueprint('api', __name__)

# ===================================================================================
# =============================== CHARACTERS ========================================
# ===================================================================================


@api.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify([char.serialize() for char in characters]), 200


@api.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200


# ===================================================================================
# =============================== LOCATIONS =========================================
# ===================================================================================
@api.route('/locations', methods=['GET'])
def get_all_locations():
    locations = Location.query.all()
    return jsonify([loc.serialize() for loc in locations]), 200


@api.route('/locations/<int:location_id>', methods=['GET'])
def get_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"error": "Location not found"}), 404
    return jsonify(location.serialize()), 200


# ===================================================================================
# ===================================== USER ========================================
# ===================================================================================
@api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id', 1)
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "characters": [char.serialize() for char in user.favorites_characters],
        "locations": [loc.serialize() for loc in user.favorites_locations]
    }), 200


# ===================================================================================
# =============================== FAVORITES =========================================
# ===================================================================================
@api.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404

    if character in user.favorites_characters:
        return jsonify({"message": "Character already in favorites"}), 400

    user.favorites_characters.append(character)
    db.session.commit()

    return jsonify({"message": "Character added to favorites"}), 201


@api.route('/favorite/location/<int:user_id>/<int:location_id>', methods=['POST'])
def add_favorite_location(user_id, location_id):
    user = User.query.get(user_id)
    location = Location.query.get(location_id)

    if not user or not location:
        return jsonify({"error": "User or Location not found"}), 404

    if location in user.favorites_locations:
        return jsonify({"message": "Location already in favorites"}), 400

    user.favorites_locations.append(location)
    db.session.commit()

    return jsonify({"message": "Location added to favorites"}), 201


@api.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404

    if character not in user.favorites_characters:
        return jsonify({"error": "Character not in favorites"}), 400

    user.favorites_characters.remove(character)
    db.session.commit()

    return jsonify({"message": "Character removed from favorites"}), 200


@api.route('/favorite/location/<int:user_id>/<int:location_id>', methods=['DELETE'])
def remove_favorite_location(user_id, location_id):
    user = User.query.get(user_id)
    location = Location.query.get(location_id)

    if not user or not location:
        return jsonify({"error": "User or Location not found"}), 404

    if location not in user.favorites_locations:
        return jsonify({"error": "Location not in favorites"}), 400

    user.favorites_locations.remove(location)
    db.session.commit()

    return jsonify({"message": "Location removed from favorites"}), 200