import base64
import requests

CLIENT_ID = "9f2e164958a1419d93e09f3c2ea3379f"
CLIENT_SECRET = "79266eaf7b1a4cc5b8f3d1beccd09cbe"

# Encode the client ID and client secret
auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
auth_bytes = auth_string.encode("utf-8")
auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

# Request an access token
token_url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {auth_base64}"
}
data = {
    "grant_type": "client_credentials"
}

response = requests.post(token_url, headers=headers, data=data)
print(response.text)
access_token = response.json()["access_token"]

artist_name = "Taylor Swift"
search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist"
headers = {
    "Authorization": f"Bearer {access_token}"
}
response = requests.get(search_url, headers=headers)
artist_data = response.json()

artist_id = "06HL4z0CvFAxyc27GXpf02"
top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
headers = {
    "Authorization": f"Bearer {access_token}"
}
response = requests.get(top_tracks_url, headers=headers)
top_tracks_data = response.json()

if "tracks" in top_tracks_data:
    tracks = top_tracks_data["tracks"]
    top_songs = [track["name"] for track in tracks]

    # Display the top songs in a list
    print("Top Songs:")
    for idx, song in enumerate(top_songs):
        print(f"{idx + 1}. {song}")
else:
    print("No tracks data found.")


category_id = "decades"  # Spotify category for "Decades"
playlist_limit = 10  # Limit the number of playlists you want to retrieve

headers = {
    "Authorization": f"Bearer {access_token}"
}

# Get a list of playlists in the "2010s" category
endpoint = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists"
params = {
    "limit": playlist_limit
}

response = requests.get(endpoint, headers=headers, params=params)
playlists_data = response.json()

if "playlists" in playlists_data:
    playlists = playlists_data["playlists"]["items"]
    if playlists:
        for idx, playlist in enumerate(playlists):
            print(f"{idx + 1}. {playlist['name']} - {playlist['id']}")
    else:
        print("No playlists found in the '2010s' category.")
else:
    print("No playlist data found.")
