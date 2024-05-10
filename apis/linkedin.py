import os

import requests
from flask import Blueprint, redirect, request, session, url_for
from requests_oauthlib import OAuth1Session

linkedin_api = Blueprint("linkedin_api", __name__)

client_id = os.getenv("LINKED_CLIENT_ID")
client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")


@linkedin_api.route("/login", methods=["GET", "POST"])
def login():
    client_id = os.getenv("LINKEDIN_CLIENT_ID")
    redirect_uri = 'http://localhost:5000/linkedin/callback'
    response_type = 'code'
    state = 'teststate'
    scope = 'openid profile email w_member_social'

    session['linkedin_state'] = state

    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}"

    return redirect(auth_url)


@linkedin_api.route("/callback", methods=["GET", "POST"])
def linkedin_callback():
    # Check for state mismatch to prevent CSRF attacks
    print("SUP GS")
    print(session.get("linkedin_state"))
    if request.args.get('state') != session.get('linkedin_state'):
        return 'Invalid state', 400

    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': os.getenv("LINKEDIN_CLIENT_ID"),
        'client_secret': os.getenv("LINKEDIN_CLIENT_SECRET"),
        'redirect_uri': 'http://localhost:5000/linkedin/callback'
    }
    response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data=data)
    if response.status_code == 200:
        access_token = response.json()['access_token']

        session['linkedin_token'] = access_token
        print("response")
        print(response.json())
        return response.json()
    else:
        return 'Failed to obtain access token'


@linkedin_api.route('/post_content')
def post_content():
    if 'linkedin_token' not in session:
        return redirect(url_for('linkedin_login'))

    access_token = session['linkedin_token']
    url = 'https://api.linkedin.com/v2/userinfo'

    # Set the headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
    }

    response = requests.get(url, headers=headers)
    print("____________________________")
    data = response.json()
    print(data)

    linkedin_id = data.get('id')
    print(f"LinkedIn User ID: {linkedin_id}")

    access_token = session['linkedin_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json',
    }

    post_data = {
            "author": "urn:li:person:KQommIGzr1",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": "This is a test post"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }


    response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=post_data)

    if response.status_code == 201:
        return 'Content posted successfully!'
    else:
        return f'Error posting content: {response.text} {access_token}', response.status_code


@linkedin_api.route('/hello')
def hello():
    return "hello"
