from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Iterable, NamedTuple, List
import time


class Track(NamedTuple):

    uri: str
    name: str
    features: List[str]
    popularity: int


    @classmethod
    def from_spotify(cls, spotify: Spotify, track: dict) -> 'Track':
        uri: str = track["track"]["uri"]
        return cls(
            uri=uri,
            name=track["track"]["name"],
            features=spotify.audio_features(uri),
            popularity=track["track"]["popularity"]
        )


def get_playlist_uri(playlist_link: str):
    # this should use url_parse or something...
    return playlist_link.split("/")[-1].split("?")[0]


def get_tracks_from_playlist(client: Spotify, playlist_name: str) -> Iterable[Track]:
    for track in client.playlist_tracks(playlist_name)["items"]:
        yield Track.from_spotify(client, track)


if __name__ == "__main__":
    CLIENT_ID = "25b56816c7b3408db0e786884e0b65ee"
    CLIENT_SECRET = "ce27527bba0e42778755095ee5cb9a91"
    # PLAYLIST_LINK = "https://open.spotify.com/playlist/37i9dQZF1EQqedj0y9Uwvu"
    PLAYLIST_LINK = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"

    client = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    spotify = Spotify(client_credentials_manager=client)

    playlist = get_playlist_uri(PLAYLIST_LINK)
    tracks = tuple(get_tracks_from_playlist(spotify, playlist))

    tempo = []
    energy = []
    danceability = []

    print(tracks[0].popularity)

    time.sleep(2)
    # print(tracks[0].uri)
    # track = spotify.track("3rUGC1vUpkDG9CZFHMur1t")
    # print(track["popularity"])
    # print(track["total"])
          

    for i in range(len(tracks)):
        tempo.append(tracks[i].features[0]["tempo"])
        energy.append(tracks[i].features[0]["energy"])
        danceability.append(tracks[i].features[0]["danceability"])

    for i in range(len(tracks)):
        print(f"Song {i + 1}. {tracks[i].name}, Tempo: {tempo[i]}, Energy: {energy[i]}, Danceability: {danceability[i]}")
