import datetime
import logging

from flask import Blueprint, Response, jsonify, request

from app.commom.form import CreateStoreForm, UpdateStoreForm
from app.commom.utils import str2bool
from app.models import Store, store_schema, stores_schema

store_controller = Blueprint('store_v1', __name__)
disable_threshold = 2
logger = logging.getLogger(__name__)


@store_controller.route('/store/<int:sid>', methods=['GET'])
def get_store(sid: int) -> Response:

    store = Store.read(sid)
    if store:
        result = store_schema.dump(store)
        return jsonify(result.data), 201
    return Response(status=404)


@store_controller.route('/store/list', methods=['GET'])
def get_store_list() -> Response:

    try:
        args = request.args
        lat = args['lat']
        lng = args['lng']
        name = args.get('name', '')
        radius = args.get('radius', 5000.0)
        page = args.get('page', 1)
        store_list, count = Store.read_list(lat=lat,
                                            lng=lng,
                                            name=name,
                                            radius=radius,
                                            page=page)
        result = stores_schema.dump(store_list)
        return jsonify({
            'result': result.data,
            'total': count
        }), 200
    except KeyError:
        return Response(status=400)
    except Exception as e:
        print(e)
        return Response(status=500)


@store_controller.route('/store', methods=['POST'])
def create_store() -> Response:

    form = CreateStoreForm(request.form)

    if form.validate_on_submit():
        if request.headers.getlist("X-Forwarded-For"):
            last_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            last_ip = request.remote_addr

        store = Store(name=form.data['name'],
                      lat=float(form.data['lat']),
                      lng=float(form.data['lng']),
                      address=form.data['address'],
                      switchable=str2bool(form.data['switchable']),
                      last_ip=last_ip)
        success = store.create()

        if success:
            result = store_schema.dump(store)
            return jsonify(result.data), 201
        else:
            return Response(status=500)
    else:
        logger.error(str(form.errors))
        return Response(status=400)


@store_controller.route('/store/<int:sid>', methods=['PUT'])
def edit_store(sid: int) -> Response:

    form = UpdateStoreForm(request.form)

    if form.validate():
        store = Store.read(sid)
        if store:
            store_json = store_schema.dump(store).data

            store.name = form.data['name'] or store_json['name']

            lat = form.data['lat'] or store_json['location'][0]
            lng = form.data['lng'] or store_json['location'][1]

            store.geom = 'POINT({lat} {lng})'.format(lat=lat, lng=lng)

            store.address = form.data['address'] or store_json['address']

            store.switchable = str2bool(
                form.data['switchable'] or store_json['switchable'])

            store.lastModified = datetime.datetime.now()
            if request.headers.getlist("X-Forwarded-For"):
                store.last_ip = request.headers.getlist("X-Forwarded-For")[0]
            else:
                store.last_ip = request.remote_addr

            success = store.update()

            if success:
                result = store_schema.dump(store)
                return jsonify(result.data), 201
            else:
                return Response(status=500)
        else:
            return Response(status=404)
    else:
        return Response(status=400)


@store_controller.route('store/<int:sid>', methods=['DELETE'])
def delete_store(sid):

    store = Store.read(sid)

    if store:
        store.disable_vote += 1
        vote_sum = sum(
            channel_vote.vote_count for channel_vote in store.votes)

        store.lastModified = datetime.datetime.now()
        if request.headers.getlist("X-Forwarded-For"):
            store.last_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
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
