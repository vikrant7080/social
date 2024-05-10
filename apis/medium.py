from flask import request, Blueprint
import requests

medium_api = Blueprint('meidum_api', __name__)


@medium_api.route("/me", methods=['GET'])
def me():
    token = "25f9ca90625717d260f56f5a800abe64e18b2a1c77e1cec2f1a2932e062a954bd"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8'
    }
    response = requests.get('https://api.medium.com/v1/me', headers=headers)
    if response.status_code == 200:
        # Print the response content (JSON data)
        print(response.json())
        return "error"
    else:
        # Print the error message if the request failed
        print('Error:', response)
        return response.text


@medium_api.route("/test", methods=['GET'])
def test():
    return "hello there!"
