from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


from typing import Iterable, NamedTuple, List


class Track(NamedTuple):

    uri: str
    name: str
    features: List[str]

    @classmethod
    def from_spotify(cls, spotify: Spotify, track: dict) -> 'Track':
        uri: str = track["track"]["uri"]
        return cls(
            uri=uri,
            name=track["track"]["name"],
            features=spotify.audio_features(uri)
        )


def get_playlist_uri(playlist_link: str):
    # this should use url_parse or something...
    return playlist_link.split("/")[-1].split("?")[0]


def get_tracks_from_playlist(client: Spotify, playlist_name: str) -> Iterable[Track]:
    for track in client.playlist_tracks(playlist_name)["items"]:
        yield Track.from_spotify(client, track)


if __name__ == "__main__":
    CLIENT_ID = "9f2e164958a1419d93e09f3c2ea3379f"
    CLIENT_SECRET = "79266eaf7b1a4cc5b8f3d1beccd09cbe"
    # PLAYLIST_LINK = "https://open.spotify.com/playlist/37i9dQZF1EQqedj0y9Uwvu"
    PLAYLIST_LINK = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"

    client = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    spotify = Spotify(client_credentials_manager=client)

    playlist = get_playlist_uri(PLAYLIST_LINK)
    tracks = tuple(get_tracks_from_playlist(spotify, playlist))

    tempo = []
    energy = []
    danceability = []
    for i in range(len(tracks)):
        tempo.append(tracks[i].features[0]["tempo"])
        energy.append(tracks[i].features[0]["energy"])
        danceability.append(tracks[i].features[0]["danceability"])

    for i in range(len(tracks)):
        print(f"Song {i + 1}. {tracks[i].name}, Tempo: {tempo[i]}, Energy: {energy[i]}, Danceability: {danceability[i]}")
