import requests
from flask import Flask, redirect, request, jsonify
import secrets
import base64
import urllib.parse
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


# Election Prediction App 
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
access_token = ""

@app.route('/login')
def login():
    state = secrets.token_urlsafe(16)
    scope = 'user-read-private user-read-email'

    query_params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    }

    query_string = urllib.parse.urlencode(query_params)
    auth_url = f'https://accounts.spotify.com/authorize?{query_string}'
    
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code', None)
    state = request.args.get('state', None)

    if state is None:
        return redirect('/#' + urlencode({'error': 'state_mismatch'}))

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        },
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        }
    }

    response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
    if response.status_code != 200:
        return redirect('/#' + urlencode({'error': 'invalid_token'}))
    
    data = response.json()
    access_token = data["access_token"]
    #make a request to the spotify api to get the user's top 5 artists
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = 'https://api.spotify.com/v1/me/top/artists?limit=5'
    response = requests.get(url, headers=headers)
    #from this response get the 5 artist names and store into a list
    artists = []
    for artist in response.json()['items']:
        artists.append(artist['name'])
    return jsonify(artists)


@app.route('/refresh_token')
def refresh_token():
    refresh_token = request.args.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Missing refresh token'}), 400

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_encoded = base64.b64encode(auth_bytes).decode('utf-8')
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_encoded}'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    url = 'https://accounts.spotify.com/api/token'

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        body = response.json()
        access_token = body.get('access_token', None)
        refresh_token = body.get('refresh_token', None)  # Sometimes the refresh token might not be returned
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token or 'No new refresh token'
        })
    else:
        return jsonify({'error': 'Failed to refresh token'}), response.status_code



if __name__ == '__main__':
    app.run(port=8888)

