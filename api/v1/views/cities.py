#!/usr/bin/python3
"""
route for handling City objects and operations
"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """
    retrieves all City objects associated with a State
    """
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """
    retrieves a City object by its ID
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    deletes a City object by its ID
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_cities(state_id):
    """
    creates a new City object associated with a State
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get(State, state_id)

    if not state:
        return abort(404)

    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    if 'name' not in data:
        return abort(400, 'Missing name')
    data['state_id'] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_cities(city_id):
    """
    updates a City object by its ID
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')

    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            return abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        return abort(404)
