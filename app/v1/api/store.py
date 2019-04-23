import datetime

from flask import Blueprint, Response, current_app, jsonify, request

from app.commom.utils import str2bool
from app.models import Store, store_schema, stores_schema

store_controller = Blueprint('store_v1', __name__)

disable_threshold = 2


@store_controller.route('/store/<int:sid>', methods=['GET'])
def get_store(sid: int) -> Response:

    store = Store.read(sid)
    if store:
        result = store_schema.dump(store)
        return jsonify(result.data), 200
    return Response(status=404)


@store_controller.route('/store/list', methods=['GET'])
def get_store_list() -> Response:

    try:
        args = request.args
        lat = args.get('lat', 0.0)
        lng = args.get('lng', 0.0)
        name = args.get('name', '')
        radius = args.get('radius', 5000.0)
        page = args.get('page', 1)
        store_list = Store.read_list(lat=lat,
                                     lng=lng,
                                     name=name,
                                     radius=radius,
                                     page=page)
        result = stores_schema.dump(store_list)
        return jsonify(result.data), 200
    except Exception as e:
        print(e)
        return Response(status=500)


@store_controller.route('/store', methods=['POST'])
def create_store() -> Response:

    request_data = request.form

    if 'name' not in request_data or \
        'lat' not in request_data or \
        'lng' not in request_data or \
        'address' not in request_data or \
            'switchable' not in request_data:
        return Response(status=400)

    store = Store(name=request_data['name'],
                  lat=float(request_data['lat']),
                  lng=float(request_data['lng']),
                  address=request_data['address'],
                  switchable=str2bool(request_data['switchable']),
                  last_ip=request.remote_addr)
    success = store.create()

    if success:
        result = store_schema.dump(store)
        return jsonify(result.data), 201
    else:
        return Response(status=500)


@store_controller.route('/store/<int:sid>', methods=['PUT'])
def edit_store(sid: int) -> Response:

    store = Store.read(sid)

    if store:
        request_data = request.form
        store_json = store_schema.dump(store).data
        store.name = request_data.get('name', store_json['name'])

        lat, lng = request_data.get(
            'lat', store_json['geom'][0]), request_data.get('lng', store_json['geom'][1])
        store.geom = 'POINT({lat} {lng})'.format(lat=lat, lng=lng)

        store.address = request_data.get('address', store_json['address'])

        store.switchable = str2bool(
            request_data.get('switchable', str(store_json['switchable'])))

        store.lastModified = datetime.datetime.now()
        store.last_ip = request.remote_addr
        success = store.update()

        if success:
            result = store_schema.dump(store)
            return jsonify(result.data), 201
        else:
            return Response(status=500)
    else:
        return Response(status=404)


@store_controller.route('store/<int:sid>', methods=['DELETE'])
def delete_store(sid):

    store = Store.read(sid)

    if store:
        store.disable_vote += 1
        vote_sum = sum(
            channel_vote.vote_count for channel_vote in store.votes)

        store.lastModified = datetime.datetime.now()
        store.last_ip = request.remote_addr

        if store.disable_vote >= vote_sum * disable_threshold:
            store.enable = False
        success = store.update()
        if success:
            if store.enable:
                result = store_schema.dump(store)
                return jsonify(result.data), 204
            else:
                return jsonify({}), 204
        else:
            return Response(status=500)
    return Response(status=404)
