#!/usr/bin/python3
"""
route for handling Amenities objects and operations from places
"""

from flask import jsonify, abort, request
from models.amenity import Amenity
from models.place import Place
from models import storage
from api.v1.views import app_views
from os import environ


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_to_place(place_id=None, amenity_id=None):
    """Handles http requests with id for amenties linked with places"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        if (amenity not in place.amenities and
                amenity.id not in place.amenities):
            abort(404)
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.pop(amenity.id, None)
        place.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if (amenity in place.amenities or
                amenity.id in place.amenities):
            return jsonify(amenity.to_dict()), 200
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            place.amenities.append(amenity)
        else:
            place.amenities = amenity
        place.save()
        return jsonify(amenity.to_dict()), 201
    