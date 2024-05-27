#!/usr/bin/python3
"""
route for handling Reviews objects and operations
"""

from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_place_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    review_list = []
    for key, value in storage.all(Review).items():
        if value.place_id == place_id:
            review_list.append(value.to_dict())
    return jsonify(review_list)

@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        return abort(404)

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    if 'user_id' not in data:
        return abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)
    
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)

    if 'text' not in data:
        return abort(400, 'Missing text')

    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        return abort(404)