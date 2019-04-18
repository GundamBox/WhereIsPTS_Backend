import datetime
from flask import Blueprint, current_app, jsonify, request, Response

from app.models import Store
from app.utils.common import str2bool
store = Blueprint('store', __name__)


@store.route('/api/store/<int:store_id>', methods=['GET'])
def get_store(store_id):
    store = Store.get_by_id(store_id)
    if store
    return jsonify(store.serialize()), 200
    else:
        return Response(status=404)


@store.route('/api/store', methods=['POST'])
def create_store():
    request_data = request.form
    store = Store(request_data['name'],
                  float(request_data['lat']),
                  float(request_data['lng']),
                  request_data['address'],
                  request_data['news'],
                  str2bool(request_data['switchable']),
                  request.remote_addr)
    success = store.create()
    if success:
        return store.id, 200
    else:
        return Response(status=400)


@store.route('/api/store/<int:store_id>', methods=['PUT'])
def edit_store(store_id):
    request_data = request.form

    s = Store.get_by_id(store_id)
    s.name = request_data['name']
    s.lat = float(request_data['lat'])
    s.lng = float(request_data['lng'])
    s.address = request_data['address']
    s.news = request_data['news']
    s.switchable = str2bool(request_data['switchable'])
    s.lastModified = datetime.datetime.now()
    s.ip = request.remote_addr

    success = s.update()

    if success:
        return Response(status=200)
    else:
        return Response(status=400)
