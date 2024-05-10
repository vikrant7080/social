from flask import Blueprint, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()

devto_api = Blueprint('devto_api', __name__)
api_key = os.getenv("DEVTO_API_KEY")

headers = {
    'Content-Type': 'application/json',
    'api-key': api_key,

}


@devto_api.route("/me", methods=['GET', 'POST'])
def me():
    response = requests.get("https://dev.to/api/articles/me", headers=headers)
    # print(response.json())
    articles = response.json()
    for article in articles:
        url = article.get('title')
        if url:
            print(url)
    return jsonify(response.json())


@devto_api.route("/post", methods=['GET', 'POST'])
def post():
    payload = {

        "article": {
            "title": "Hello, World!",
            "published": True,
            "body_markdown": "Hello DEV, this is my first post",
            "tags": [
                "discuss",
                "help"
            ],
            "series": "Hello series"
        }

    }
    response = requests.post("https://dev.to/api/articles", json=payload, headers=headers)
    print(response.text)
    return jsonify(response.text)
