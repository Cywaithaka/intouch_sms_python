# -*- coding: utf-8 -*-
import json
import requests
import logging

username = "" # intouch username
password = "" # intouch user password
sender_id = "Intouchvas" # Sender SMS Shortcode
msisdn = "+254721458132" # Recipient number 
api_token = "generated_api_key"

SUCCESS_CODES = [200, 202]

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

def action_generate_access_token(_user, _pass):
    """
    Generate an access token using provided username and password. Returns the token if successful,
    otherwise logs an error and returns False.

    Parameters:
    - _user (str): Username for authentication.
    - _pass (str): Password for authentication.

    Returns:
    - str or False: Generated access token if successful, False otherwise.
    """
    auth_url = "https://identity-service.intouchvas.io/auth/api-key"
    generated_auth=requests.auth.HTTPBasicAuth(_user,_pass)
    headers = {'Content-type': 'application/json', 'Authorization': f'Basic {generated_auth}'}
    try:
        response = requests.request("GET", auth_url,headers=headers, auth=generated_auth)
        if response.status_code in SUCCESS_CODES:
            _token = response.json().get('token')
            if _token:
                return _token
        else:
            _logger.error(f"Failed to generate token with username: {_user} and Password: {_pass} {response.text}")
    except Exception as e:
        _logger.error(f"Error getting an access token {e}")
    return False



def action_send_sms():
    """
    Constructs a JSON payload with message details and sends an SMS.
    If the API token is invalid (401), it attempts to
    regenerate the token and resend the SMS.

    Parameters:
    - None (necessary variables like api_token, msisdn, sender_id, etc., are in the scope)

    Returns:
    - None: Logs status code and response text.
    """
    newHeaders = {
        'Content-type': 'application/json', 
        'api-key': api_token
        }
    payload = json.dumps({
        "message": "Test message 2",
        "msisdn": msisdn,
        "sender_id": sender_id,
        "callback_url": "https://callback.io/123/dlr"
        })
    transactional_url = 'https://sms-service.intouchvas.io/message/send/transactional'
    response = requests.request("POST", transactional_url, data=payload,headers=newHeaders)
    if response.status_code == 401:
        _logger.info("Having issues with the existing token. Regenerate")
        new_token = action_generate_access_token(username, password)
        newHeaders['api-key'] = new_token
        response = requests.request("POST", transactional_url, data=payload,headers=newHeaders)
    _logger.info(f"Status code: {response.status_code}")
    _logger.info(response.text)

if __name__ == '__main__':
    action_send_sms()
