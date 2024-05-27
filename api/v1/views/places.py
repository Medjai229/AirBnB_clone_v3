#!/usr/bin/python3
"""
route for handling Place objects and operations
"""

from flask import jsonify, abort, request
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city(city_id):
    """
    retrieves all City objects associated with a State
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """
    retrieves the places objects
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    retrieves the places objects
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    retrieves the places objects
    """
    city = storage.get(City, city_id)

    if not city:
        return abort(404)

    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        return abort(400, 'Missing name')

    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    retrieves the places objects
    """
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        return abort(404)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    retrieves the places objects based on provided JSON search
    """
    if request.content_type != 'application/json':
        return abort(400, "NOt a JSON")
    if not request.get_json():
        return abort(400, "NOt a JSON")

    data = request.get_json()

    if data:
        states = data.get('states')
        cities = data.get('cities')
        amenities = data.get('amenities')
    if not (states or cities or amenities):
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)
    list_places = []

    if states:
        states_obj = [storage.get(State, state_id) for state_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, city_id) for city_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            all_places = storage.all(Place).values()
            amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
            for place in all_places:
                if all([am in place.amenities for am in amenities_obj]):
                    list_places.append(place)

    places = []
    for plc_Obj in list_places:
        plc_dict = plc_Obj.to_dict()
        plc_dict.pop('amentites', None)
        places.append(plc_dict)
    return jsonify(places)
