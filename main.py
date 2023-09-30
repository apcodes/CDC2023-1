import json
from dotenv import load_dotenv
import os
import base64
from requests import get, post

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"  # Remove spaces around ':'
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + auth_base64, "Content-Type": "application/x-www-form-urlencoded"}

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)

    if result.status_code == 200:
        try:
            json_result = json.loads(result.content)
            return json_result.get("access_token")
        except json.decoder.JSONDecodeError:
            print("Error decoding JSON response")
            return None
    else:
        print(f"Error: {result.status_code} - Unable to get access token")
        return None

    # print(json_result)  # Print the entire response for debugging

    # return json_result.get("access_token")  # Use .get() to handle missing 'access_token'

def get_auth_header(token):
    return {"Authorization": "Bearer " + token} 

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    print(json_result)  # Print the entire response for debugging

    # Check if the expected data structure is different from what you anticipated
    if "tracks" not in json_result:
        print("Unexpected API response structure")
        return None

    json_items = json_result["tracks"]["items"]

    if len(json_items) == 0:
        print("No artist with that name exists")
        return None

    return json_items[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)

    # print(result.content)  # Print the API response for debugging

    if result.status_code == 200:
        try:
            json_results = json.loads(result.content)["tracks"]
            return json_results
        except KeyError:
            print("Unexpected API response structure")
            return None
    else:
        print(f"Error: {result.status_code} - Unable to fetch top tracks")
        return None

# token = get_token()
# result = search_for_artist(token, "Taylor Swift")
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)

# # for idx, song in enumerate(songs):
# #     print(f"{idx + 1}. {song['name']}")