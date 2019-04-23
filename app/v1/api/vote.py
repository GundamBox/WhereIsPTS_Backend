import datetime

from flask import Blueprint, Response, current_app, jsonify, request

from app.models import Vote, Store, Channel

vote_controller = Blueprint('vote_v1', __name__)


@vote_controller.route('/vote/store/<int:sid>', methods=['POST'])
def vote_store_channel(sid):

    store = Store.read(sid)
    if store:
        request_data = request.form
        cid = request_data['cid']

        idx = -1
        for i, channel in enumerate(store.channels):
            if channel.cid == cid:
                idx = i
                break
        if idx >= 0:
            store.votes[idx].vote_count += 1
        else:
            channel = Channel.read(cid)
            vote = Vote(sid, cid, 1)
            if channel:
                Vote.create(vote)
                return str(store.sid), 200

    return Response(status=404)
