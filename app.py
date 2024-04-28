import requests
from flask import Flask, redirect, request, jsonify, render_template
import secrets
import base64
import urllib.parse
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from db import fetch_google_trends, store_in_database, get_db
import pandas as pd

# Explicitly set Jinja2 as the template engine

app = Flask(__name__)
# Explicitly set Jinja2 as the template engine
app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'
load_dotenv()


# Election Prediction App 
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
access_token = ""

@app.route('/login')
def login():
    state = secrets.token_urlsafe(16)
    scope = 'user-top-read'

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

    # URL and Headers for requesting the access token
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    body = {
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    # Perform the POST request to get the access token
    response = requests.post(url, data=body, headers=headers)
    print(f"Request for Access Token: POST {url}")
    print(f"Headers: {headers}")
    print(f"Body: {body}")
    
    if response.status_code != 200:
        print(f"Failed to retrieve access token: {response.text}")
        return redirect('/#' + urlencode({'error': 'invalid_token'}))
    
    # Parse the access token from the response
    data = response.json()
    access_token = data["access_token"]
    print(f"Access Token: {access_token}")

    # Fetch top artists using the access token
    artist_data = fetch_Artists(access_token)
    print(f"Top Artists Data: {artist_data}")
    
    # Fetch Google Trends data
    state_data = pd.DataFrame()
    for keyword in artist_data:
        df = fetch_google_trends(keyword)
        #store_in_database(keyword, df, get_db())
        state_data = pd.concat([state_data, df], axis=1)
    
    #get the 5 indexes with the highest values in each column and store them in a new dataframe
    state_data = state_data.apply(lambda x: x.nlargest(5).index)
    #get a list of the 1st row of the dataframe
    state_data = state_data.iloc[0].tolist()
    print(state_data)


    # Display the data
    return display_data(state_data)
    #return jsonify(artist_data)


#create a function that callback can call to direct the user to a page/end point that will display the data in a more user friendly way
@app.route('/display_data')
def display_data(state_data):
    #create a front end page that will display the data
    return render_template('index.html', data=state_data)
    

    





def fetch_Artists(access_token):
    print("----")
    print(access_token)
    print("----")
    url = 'https://api.spotify.com/v1/me/top/artists?limit=5'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    print(f"Response Data: {response.text}")  # This will show what Spotify actually returned

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            artists = [artist['name'] for artist in data['items']]
            return artists
        else:
            return {'error': 'No items found in data', 'data': data}
    else:
        return {'error': 'Failed to retrieve artists', 'status_code': response.status_code}


"""
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

"""

if __name__ == '__main__':
    app.run(port=8888, debug=True)

