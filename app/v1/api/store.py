import datetime

from flask import Blueprint, Response, current_app, jsonify, request

from app.commom.utils import str2bool
from app.models import Store

store_controller = Blueprint('store_v1', __name__)

disable_threshold = 2


@store_controller.route('/store/<int:sid>', methods=['GET'])
def get_store(sid: int) -> Response:

    store = Store.read(sid)
    if store:
        return jsonify(store.serialize()), 200
    return Response(status=404)


@store_controller.route('/store/list', methods=['GET'])
def get_store_list() -> Response:

    args = request.args
    store_list = Store.read_list(args)
    return jsonify(store_list.serialize()), 200


@store_controller.route('/store', methods=['POST'])
def create_store() -> Response:

    request_data = request.form
    store = Store(request_data['name'],
                  float(request_data['lat']),
                  float(request_data['lng']),
                  request_data['address'],
                  str2bool(request_data['switchable']),
                  request.remote_addr)
    success = store.create()

    if success:
        return str(store.sid), 200
    else:
        return Response(status=500)


@store_controller.route('/store/<int:sid>', methods=['PUT'])
def edit_store(sid: int) -> Response:

    store = Store.read(sid)

    if store:
        request_data = request.form
        store.name = request_data['name']
        store.lat = float(request_data['lat'])
        store.lng = float(request_data['lng'])
        store.address = request_data['address']
        store.switchable = str2bool(request_data['switchable'])
        store.lastModified = datetime.datetime.now()
        store.ip = request.remote_addr

        success = store.update()

        if success:
            return str(store.sid), 200
        else:
            return Response(status=500)
    else:
        return Response(status=404)


@store_controller.route('store/<int:sid>', methods=['DELETE'])
def delete_store(sid):

    store = Store.read(sid)

    if store:
        store.disable_vote += 1
        vote_sum = sum(channel_vote.vote_count for channel_vote in store.votes)
        if store.disable_vote * disable_threshold >= vote_sum:
            store.enable = False
            store.update()
            return jsonify(store.serialize()), 200

    return Response(status=404)
