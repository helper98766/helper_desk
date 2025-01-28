def get_token_field_from_auth_response(self, response):
    if response:
        if 'access_token' in response:
            return response['access_token']
        elif 'token' in response:
            return response['token']
        elif 'response' in response:
            return response['response']
        elif 'systemToken' in response:
            return response['systemToken']
        elif 'authentication' in response:
            return response['authentication']['token']
        else:
            return Exception("IP address are not valid", status_code=403)