import unittest
from mib import create_app
import responses



class ResourcesTest(unittest.TestCase):

    @responses.activate
    def test_blacklist_logic(self):
        
        # creating an app instace to run test activities
        tested_app = create_app()
        
        USERS_ENDPOINT = tested_app.config['USERS_MS_URL']
        
        app = tested_app.test_client()

        unexisting_blocking_user = 3
        unavailable_blocked_user = 5
        existing_blocking_user = 1
        available_blocked_user = 2

        json_data_failure = {
                        'blocked_user_id': int(unavailable_blocked_user),
                        'requester_id': int(unexisting_blocking_user)
                        }
        json_data_failure2 = {
                        'blocked_user_id': int(unavailable_blocked_user),
                        'requester_id': int(existing_blocking_user)
                        }
        json_data_success = {
                        'blocked_user_id': available_blocked_user,
                        'requester_id': existing_blocking_user
                        }
        # failure without users response not already mocked, status_code 500
        response = app.post('/block',json=json_data_success)
        self.assertEqual(response.status_code,500)

        responses.add(responses.GET, "%s/users/%s" % (USERS_ENDPOINT, str(unexisting_blocking_user)),
                  json={'status': 'Current user not present'}, status=404)

        responses.add(responses.GET, "%s/users/%s" % (USERS_ENDPOINT, str(unavailable_blocked_user)),
                  json={'status': 'User not present'}, status=404)

        responses.add(responses.GET, "%s/users/%s" % (USERS_ENDPOINT, str(existing_blocking_user)),
                   status=200)

        responses.add(responses.GET, "%s/users/%s" % (USERS_ENDPOINT, str(available_blocked_user)),
                   status=200)
        

        # BLOCK FAILURE WHEN CURRENT USER DOESN'T EXIST
        response = app.post('/block',json=json_data_failure)
        self.assertEqual(response.status_code,404)

        # BLOCK FAILURE WHEN OTHER USER DOESN'T EXIST
        response = app.post('/block',json=json_data_failure2)
        self.assertEqual(response.status_code,404)

        # BLOCK SUCCESS
        response = app.post('/block',json=json_data_success)
        self.assertEqual(response.status_code,201)

        # BLACKLIST retrieving
        # checking the istances on database
        response = app.get('/blacklist', json = {'requester_id' : existing_blocking_user})
        self.assertEqual(response.status_code,200)
        response_json = response.get_json()
        self.assertEqual(response_json['blacklist'],[2])
    
        # UNBLOCK SUCCESS
        # removing the previously created istance from blacklist table
        response = app.delete('/unblock',json=json_data_success)
        self.assertEqual(response.status_code,202)
            
        # UNBLOCK FAILURE
        # removing again the previously created istance from blacklist table
        response = app.delete('/unblock',json=json_data_success)
        self.assertEqual(response.status_code,404)
            