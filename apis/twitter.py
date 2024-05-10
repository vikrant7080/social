import os
import json
from flask import Blueprint, redirect, request, session, url_for
from requests_oauthlib import OAuth1Session

twitter_api = Blueprint('twitter_api', __name__)

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_CALLBACK_URL = 'http://localhost:5000/twitter/callback'

oauth = OAuth1Session(
    client_key=TWITTER_API_KEY,
    client_secret=TWITTER_API_SECRET,
    callback_uri=TWITTER_CALLBACK_URL
)


@twitter_api.route('/login')
def twitter_login():
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    session['resource_owner_key'] = resource_owner_key
    session['resource_owner_secret'] = resource_owner_secret

    authorization_url = oauth.authorization_url('https://api.twitter.com/oauth/authenticate')
    return redirect(authorization_url)


@twitter_api.route('/callback')
def twitter_callback():
    if 'resource_owner_key' not in session:
        return 'Error: Request token missing in session', 400

    verifier = request.args.get('oauth_verifier')
    if not verifier:
        return 'Error: OAuth verifier missing', 400

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url, verifier=verifier)

    session['twitter_access_token'] = oauth_tokens.get('oauth_token')
    session['twitter_access_token_secret'] = oauth_tokens.get('oauth_token_secret')

    return "You are logged in on X "


@twitter_api.route('/post_tweet', methods=['GET', 'POST'])
def post_tweet():
    # tweet_text = request.json.get('tweet_text')
    # if not tweet_text:
    #     return 'Error: Tweet text is required', 400
    # request.form.get('tweet_text')
    tweet_text = "hello tweet"
    oauth = OAuth1Session(
        client_key=TWITTER_API_KEY,
        client_secret=TWITTER_API_SECRET,
        resource_owner_key=session.get('twitter_access_token'),
        resource_owner_secret=session.get('twitter_access_token_secret')
    )
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'text': tweet_text
    }

    json_payload = json.dumps(payload)

    tweet_url = 'https://api.twitter.com/2/tweets'

    response = oauth.post(tweet_url, data=json_payload, headers=headers)

    if response.status_code == 200:
        return 'Tweet posted successfully!'
    else:
        return 'Error posting tweet: ' + response.text, response.status_code
