#!/usr/bin/python3
"""
route for handling Amenities objects and operations from places
"""

from flask import jsonify, abort, request
from models.amenity import Amenity
from models.place import Place
from models.engine import db_storage
from models import storage
from api.v1.views import app_views

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if isinstance(storage, DBStorage):
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if isinstance(storage, DBStorage):
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    return jsonify(amenity.to_dict()), 201