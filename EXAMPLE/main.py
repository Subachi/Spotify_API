from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()#enter your .env file path in quotes inside

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Gets authentication token to acccess API


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Gets authentication header for JSON request


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Returns items object


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)[
        "artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists...")
        return None
    return json_result[0]

# Returns base62 encoded artist ID


def get_artist_id(token, artist_name):
    url = search_for_artist(token, artist_name)["external_urls"]["spotify"]
    substr = url.split("/")
    end_point = len(substr)-1
    return substr[end_point]


'''
#Song reccomendation
def request_rec(token, seed_genres):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    query = f""
    pass
'''

artist = input("Enter name: ")
token = get_token()
print("Artist id: %s" % (get_artist_id(token, artist)))
