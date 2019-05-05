import datetime

from flask import Blueprint, Response, jsonify, request

from app.commom.utils import str2bool
from app.models import Channel, channel_schema, channels_schema

channel_controller = Blueprint('channel_v1', __name__)


@channel_controller.route('/channel/<int:cid>', methods=['GET'])
def get_channel(cid: int) -> Response:

    channel = Channel.read(cid)
    if channel:
        result = channel_schema.dump(channel)
        return jsonify(result.data), 200
    else:
        return Response(status=404)


@channel_controller.route('/channels', methods=['GET'])
def get_channel_list() -> Response:

    channel_list = Channel.read_list()
    result = channels_schema.dump(channel_list)
    return jsonify(result.data), 200


@channel_controller.route('/channel', methods=['POST'])
def create_channel():

    request_data = request.form
    channel_name = request_data['name']

    channel = Channel(channel_name)
    success = channel.create()

    if success:
        result = channel_schema.dump(channel)
        return jsonify(result.data), 201
    else:
        return Response(status=500)


@channel_controller.route('/channel/<int:cid>', methods=['PUT'])
def edit_channel(cid):

    channel = Channel.read(cid)
    if channel:

        request_data = request.form
        channel_name = request_data['name']

        channel.name = channel_name
        success = channel.update()

        if success:
            result = channel_schema.dump(channel)
            return jsonify(result.data), 201

    return Response(status=404)
