# TODO look at mib-users/mib/resources/users.py
from flask import request, jsonify
from mib.dao.blacklist_manager import BlacklistManager
from mib.models.blacklist import Blacklist
import datetime

#TODO handle errors
def block():
    post_data = request.get_json()
    blocking_user = post_data.get('blocking_user_id')
    blocked_user = post_data.get('blocked_user_id')

    blacklist = Blacklist()
    blacklist.set_blocking_user_id(blocking_user)
    blacklist.set_blocked_user_id(blocked_user)

    #TODO check if blocked_user_id exists

    BlacklistManager.block(blacklist)
    response_object = {
        'blacklist': blacklist.serialize(),
        'status': 'success',
        'message': 'Successfully added to blacklist',
    }

    return jsonify(response_object), 201

def retrieving_blacklist(user_id):
    blacklist = BlacklistManager.retrieving_blacklist(user_id)
    return jsonify(blacklist.serialize()), 200

def unblock(blocking, blocked):
    blacklist = BlacklistManager.retrieving_blacklist_element(blocking, blocked)

    BlacklistManager.unblock(blacklist)

    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }

    return jsonify(response_object), 202
