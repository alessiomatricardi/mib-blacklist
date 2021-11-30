# TODO look at mib-users/mib/resources/users.py
from flask import request, jsonify
from mib.dao.blacklist_manager import BlacklistManager
from mib.models.blacklist import Blacklist
import datetime
import json
import requests
from mib import app

USERS_ENDPOINT = app.config['USERS_MS_URL']
REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

#TODO handle errors
def block():
    post_data = request.get_json()
    blocking_user_id = post_data.get('blocking_user_id')
    blocked_user_id = post_data.get('blocked_user_id')

    # check if the users exist
    try:
        blocking_user_response = requests.get("%s/users/%s/list/%s" % (USERS_ENDPOINT, str(blocking_user_id), str(blocking_user_id)),
                                timeout=REQUESTS_TIMEOUT_SECONDS)

        blocked_user_response = requests.get("%s/users/%s/list/%s" % (USERS_ENDPOINT, str(blocking_user_id), str(blocked_user_id)),
                                timeout=REQUESTS_TIMEOUT_SECONDS)
        
        if blocking_user_response.status_code != 200:
            response_object = {
                'status': 'failure',
                'message': 'Error in retrieving blocking user',
            }
            return blocking_user_response.json(), blocking_user_response.status_code

        if blocked_user_response.status_code != 200:
            response_object = {
                'status': 'failure',
                'message': 'Error in retrieving blocked user',
            }
            return blocked_user_response.json(), blocked_user_response.status_code 
            
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        response_object = {
            'status': 'failure',
            'message': 'Error in retrieving user',
        }
        return jsonify(response_object), 500

    blacklist = Blacklist()
    blacklist.set_blocking_user_id(blocking_user_id)
    blacklist.set_blocked_user_id(blocked_user_id)

    
    try:
        BlacklistManager.block(blacklist)
    except Exception:
        response_object =  {
        'status': 'failure',
        'message': 'User not added to blacklist',
        }
        return jsonify(response_object), 500
    
    response_object = {
                'blacklist': blacklist.serialize(),
                'status': 'success',
                'message': 'Successfully added to blacklist',
            }
    return jsonify(response_object), 201
    #return jsonify(response_object), 201

def get_blacklist(user_id):
    try:
        blacklist = BlacklistManager.retrieve_blacklist_by_id(user_id)
    except Exception:
        response_object =  {
        'blacklist': None,
        'status': 'failure',
        'message': 'Blacklist retrieving failure',
        }
        return jsonify(response_object), 500
    
    response_object = {
                'blacklist': json.dumps(blacklist),
                'status': 'success',
                'message': 'Blacklist successfully retrieved',
            }
    return jsonify(response_object), 200
    

def unblock():
    post_data = request.get_json()
    blocking_user = post_data.get('blocking_user_id')
    blocked_user = post_data.get('blocked_user_id')
    blacklist = BlacklistManager.retrieve_blacklist_element(blocking_user, blocked_user)

    if not blacklist:
        response_object =  {
        'status': 'failure',
        'message': 'User not in blacklist',
        }
        return jsonify(response_object), 404

    try:
        BlacklistManager.unblock(blacklist)
    except Exception:
        response_object =  {
        'status': 'failure',
        'message': 'User not removed from blacklist',
        }
        return jsonify(response_object), 500
    
    response_object = {
        'status': 'success',
        'message': 'Successfully removed from blacklist',
    }

    return jsonify(response_object), 202
