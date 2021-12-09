from flask import request, jsonify
from mib.dao.blacklist_manager import BlacklistManager
from mib.models.blacklist import Blacklist
import datetime
import json
import requests
from mib import app

USERS_ENDPOINT = app.config['USERS_MS_URL']
REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']


def get_blacklist():

    data = request.get_json()
    requester_id = data.get('requester_id')

    blocking = []
    blocked = []
    try:
        blocking,blocked= BlacklistManager.retrieve_blacklist_by_user_id(requester_id)

    except Exception:
        response_object =  {
            'status': 'failure',
            'description': 'Blacklist retrieving failure',
        }
        return jsonify(response_object), 500

    response_object = {
        'blocking': blocking,
        'blocked': blocked,
        'status': 'success',
        'description': 'Blacklist successfully retrieved',
    }
    return jsonify(response_object), 200


def block():
    data = request.get_json()
    blocking_user_id = data.get('requester_id')
    blocked_user_id = data.get('blocked_user_id')

    # check if the users exist
    try:
        data = {'requester_id': blocking_user_id}
        blocking_user_response = requests.get(
            "%s/users/%s" % (USERS_ENDPOINT, str(blocking_user_id)),
            timeout=REQUESTS_TIMEOUT_SECONDS,
            json=data)
        
        if blocking_user_response.status_code != 200:
            response_object = {
                'status': 'failure',
                'description': 'Error in retrieving blocking user',
            }
            return blocking_user_response.json(), blocking_user_response.status_code

        blocked_user_response = requests.get(
            "%s/users/%s" % (USERS_ENDPOINT, str(blocked_user_id)),
            timeout=REQUESTS_TIMEOUT_SECONDS,
            json=data)

        if blocked_user_response.status_code != 200:
            response_object = {
                'status': 'failure',
                'description': 'Error in retrieving blocked user',
            }
            return blocked_user_response.json(), blocked_user_response.status_code

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        response_object = {
            'status': 'failure',
            'description': 'Connection error while retrieving users',
        }
        return jsonify(response_object), 500


    blacklist = Blacklist()
    blacklist.set_blocking_user_id(blocking_user_id)
    blacklist.set_blocked_user_id(blocked_user_id)

    BlacklistManager.block(blacklist)

    response_object = {
        'blacklist': blacklist.serialize(),
        'status': 'success',
        'description': 'Successfully added to blacklist',
    }
    return jsonify(response_object), 201


def unblock():
    data = request.get_json()
    blocking_user = data.get('requester_id')
    blocked_user = data.get('blocked_user_id')
    
    blacklist = BlacklistManager.retrieve_blacklist_element(blocking_user, blocked_user)
    if not blacklist:
        response_object =  {
            'status': 'failure',
            'description': 'User isn\'t blocked',
        }
        return jsonify(response_object), 404

    BlacklistManager.unblock(blacklist)

    response_object = {
        'status': 'success',
        'description': 'Successfully removed from blacklist',
    }

    return jsonify(response_object), 202
