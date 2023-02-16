#!/usr/bin/python3
"""
Views for Place model
"""
from api.v1.views import app_views
from flask import abort, jsonify, request

from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def place(place_id=None):
    """
    Place model view based on place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        for k, v in request.get_json().items():
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def city_places(city_id=None):
    """
    Place model view based on city_id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'Missing user_id'}), 400
        if not storage.get(User, user_id):
            abort(404)
        if 'name' not in data.keys():
            return jsonify({'error': 'Missing name'}), 400
        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
