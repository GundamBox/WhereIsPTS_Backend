import datetime
import logging

from flask import Blueprint, Response, current_app, jsonify, request

from app.common.exception import FlaskException
from app.common.utils import str2bool
from app.forms.store import CreateStoreForm, GetStoreListForm, UpdateStoreForm
from app.models import Store, store_schema, stores_schema

store_controller = Blueprint('store_v1', __name__)
logger = logging.getLogger(__name__)


@store_controller.route('/store/<int:sid>', methods=['GET'])
def get_store(sid: int) -> Response:
    store = Store.read(sid)
    result = store_schema.dump(store)

    return jsonify(result.data), 200


@store_controller.route('/store/list', methods=['GET'])
def get_store_list() -> Response:
    form = GetStoreListForm(request.args)

    if form.validate():
        store_list, count = Store.read_list(lat=form.data['lat'],
                                            lng=form.data['lng'],
                                            name=form.data['name'],
                                            radius=form.data['radius'],
                                            page=form.data['page'],
                                            page_size=form.data['page_size'])
        result = stores_schema.dump(store_list)

        return jsonify({
            'result': result.data,
            'total': count
        }), 200
    else:
        raise FlaskException(message=str(form.errors), status_code=400)


@store_controller.route('/store', methods=['POST'])
def create_store() -> Response:
    form = CreateStoreForm(request.form)

    if form.validate():
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
        store.create()
        result = store_schema.dump(store)

        return jsonify(result.data), 201
    else:
        raise FlaskException(message=str(form.errors), status_code=400)


@store_controller.route('/store/<int:sid>', methods=['PUT'])
def edit_store(sid: int) -> Response:
    form = UpdateStoreForm(request.form)

    if form.validate():
        store = Store.read(sid)
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

        store.update()

        result = store_schema.dump(store)
        return jsonify(result.data), 201
    else:
        raise FlaskException(message=str(form.errors), status_code=400)


@store_controller.route('store/<int:sid>', methods=['DELETE'])
def delete_store(sid):
    store = Store.read(sid)
    store.disable_vote += 1
    vote_sum = sum(
        channel_vote.vote_count for channel_vote in store.votes)

    store.lastModified = datetime.datetime.now()

    if request.headers.getlist("X-Forwarded-For"):
        store.last_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        store.last_ip = request.remote_addr

    baseline = current_app.config['REPORT_STORE_NOT_EXISTS_BASELINE']
    disable_threshold = current_app.config['DISABLE_THRESHOLD']
    if store.disable_vote >= vote_sum * disable_threshold + baseline:
        store.enable = False

    store.update()

    if store.enable:
        store_dump = store_schema.dump(store)
        store_json = jsonify(store_dump.data)
    else:
        store_json = jsonify({})

    return store_json, 204
