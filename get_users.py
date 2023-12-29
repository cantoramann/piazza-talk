import requests
import config

params = {
    'method': 'network.get_users',
}

json_data = {
    'method': 'network.get_users',
    'params': {
        'nid': config.STUDENT_NID,
    },
}

user_map = {}

def get_user_data(requested_ids = []):

    # check only for users that haven't been checked yet
    return_ids = {}
    for requested_id in requested_ids:
        if requested_id in user_map:
            return_ids[requested_id] = user_map[requested_id]
            requested_ids.remove(requested_id)

    json_data['params']['ids'] = requested_ids        
    
    response = requests.post('https://piazza.com/logic/api', params=params, cookies=config.cookies, headers=config.headers, json=json_data)
    parsed_data = response.json()

    for user in parsed_data['result']:
        user_map[user['id']] = {'role': user['role'], 'name': user['name']}
        return_ids[user['id']] =  {'role': user['role'], 'name': user['name']}

    return return_ids    
