from flask import Blueprint, current_app, jsonify, request

from app.models import Store

search = Blueprint('search_v1', __name__)


@search.route('/search/<string:name>', methods=['GET'])
def search_store(name):
    store_list = Store.search_by_name(name)
    return jsonify([store.serialize() for store in store_list]), 200


@search.route('/search/<float:lat>,<float:lng>', methods=['GET'])
def search_nearby(lat, lng):
    store_list = Store.search_by_lat_lng(float(lat), float(lng), 10.0)
    return jsonify([store.serialize() for store in store_list]), 200
