import datetime

from flask import Blueprint, Response, jsonify, request

from app.models import Channel, channel_schema, channels_schema
from app.forms.channel import CreateChannelForm, UpdateChannelForm
from app.common.exception import FlaskException

channel_controller = Blueprint('channel_v1', __name__)


@channel_controller.route('/channel/<int:cid>', methods=['GET'])
def get_channel(cid: int) -> Response:
    channel = Channel.read(cid)
    result = channel_schema.dump(channel)
    return jsonify(result.data), 200


@channel_controller.route('/channels', methods=['GET'])
def get_channel_list() -> Response:
    channel_list = Channel.read_list()
    result = channels_schema.dump(channel_list)
    return jsonify(result.data), 200


@channel_controller.route('/channel', methods=['POST'])
def create_channel():
    form = CreateChannelForm(request.form)
    if form.validate():

        channel_name = form.data['name'].strip()

        channel = Channel(channel_name)
        channel.create()

        result = channel_schema.dump(channel)
        return jsonify(result.data), 201
    else:
        raise FlaskException(message=str(form.errors), status_code=400)

@channel_controller.route('/channel/<int:cid>', methods=['PUT'])
def edit_channel(cid):
    channel = Channel.read(cid)
    form = UpdateChannelForm(request.form)

    if form.validate():
        channel_name = form.data['name'].strip()

        channel.name = channel_name
        channel.update()

        result = channel_schema.dump(channel)
        return jsonify(result.data), 201
    else:
        raise FlaskException(message=str(form.errors), status_code=400)
