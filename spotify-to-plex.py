import requests
import base64
import logging
from plexapi.server import PlexServer
import plexapi
import json
import time
import subprocess

# Setting up logging
logging.basicConfig(level=logging.INFO)

# --- Spotify Authentication ---

def get_spotify_token():
    CLIENT_ID = 'xxxxxxxxxxx'
    CLIENT_SECRET = 'xxxxxxxxxxxxxxxxxxxx'
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    auth_headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    auth_data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=auth_headers, data=auth_data)
    token_response = response.json()
    return token_response['access_token']

# --- Fetch Spotify Playlist Data ---

def get_playlist_tracks(access_token, playlist_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # First fetch the playlist name
    response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers)
    playlist_data = response.json()
    playlist_name = playlist_data['name']
    
    # Now fetch tracks (paginated)
    tracks = []
    next_page_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    
    while next_page_url:
        response = requests.get(next_page_url, headers=headers)
        track_data = response.json()
        
        for item in track_data['items']:
            tracks.append((item['track']['name'], item['track']['artists'][0]['name']))
        
        next_page_url = track_data.get('next', None)  # Move to next page if exists
    
    return playlist_name, tracks


def get_spotify_track_url(access_token, track_name, artist_name):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    search_query = f"{track_name} {artist_name}"
    response = requests.get(f"https://api.spotify.com/v1/search?q={search_query}&type=track&limit=1", headers=headers)
    search_data = response.json()
    if search_data['tracks']['items']:
        return search_data['tracks']['items'][0]['external_urls']['spotify']
    return None

# --- Plex Helper Functions ---

PLEX_SERVER_URL = 'http://localhost:32400'
PLEX_TOKEN = 'xxxxxxxxxxxxxxxxx'
plex = PlexServer(PLEX_SERVER_URL, PLEX_TOKEN)
def get_music_playlists():
    all_playlists = plex.playlists()
    music_playlists = [playlist for playlist in all_playlists if playlist.items() and isinstance(playlist.items()[0], plexapi.audio.Track)]
    return music_playlists

def test_plex_connectivity():
    try:
        music_playlists = get_music_playlists()
        if music_playlists:
            logging.info("Successfully retrieved existing music playlists from Plex:")
            for playlist in music_playlists:
                logging.info(playlist.title)
        else:
            logging.info("Connected to Plex, but no music playlists found.")
        return True
    except Exception as e:
        logging.error(f"Error connecting to Plex: {e}")
        return False





def search_plex_for_media(track_name, artist_name):
    def plex_search(query):
        try:
            return plex.search(query)
        except plexapi.exceptions.BadRequest as e:
            logging.warning(f"Failed Plex search for query '{query}'. Error: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error during Plex search for query '{query}'. Error: {e}")
            return []

    plex = PlexServer(PLEX_SERVER_URL, PLEX_TOKEN)

    # 1. Search with both track title and artist
    search_query = f"{track_name} {artist_name}"
    results = plex_search(search_query)
    tracks = [item for item in results if item.type == 'track']
    
    if tracks:
        return tracks[0].ratingKey
    
    time.sleep(0.5)  # Introduce a short delay to avoid rate-limiting

    # 2. Search only by the track title
    search_query = track_name.replace("(", "").replace(")", "").replace(".", "")  # Sanitize the input
    results = plex_search(search_query)
    tracks = [item for item in results if item.type == 'track']
    
    if tracks:
        return tracks[0].ratingKey

    time.sleep(0.5)  # Another short delay

    # 3. Search only by the artist and then filter
    search_query = artist_name
    results = plex_search(search_query)
    for item in results:
        if item.type == 'artist':
            artist_tracks = item.tracks()
            for track in artist_tracks:
                if track.title == track_name:
                    return track.ratingKey

    return None



def get_existing_playlist(name):
    """Retrieve a playlist by name. Return None if not found."""
    for playlist in plex.playlists():
        if playlist.title == name:
            return playlist
    return None


def create_plex_playlist(name, media_ids):
    """
    Create a Plex playlist with the given name and list of Plex media IDs.
    """
    tracks = [plex.fetchItem(media_id) for media_id in media_ids]
    plex.createPlaylist(name, items=tracks)


def main():
    access_token = get_spotify_token()
    logging.info("Fetched Spotify Access Token")

    if not test_plex_connectivity():
        logging.error("Exiting due to Plex connectivity issues.")
        return

    with open("playlists.json", "r") as file:
        playlists_data = json.load(file)

    # 1. Get the tracks from all the Spotify playlists
    all_spotify_tracks = []
    for playlist_url, _ in playlists_data.items():
        playlist_id = playlist_url.strip().split('/')[-1]
        _, tracks = get_playlist_tracks(access_token, playlist_id)
        all_spotify_tracks.extend(tracks)

    # 2. Determine which tracks exist in Plex
    missing_tracks = []
    for track_name, artist_name in all_spotify_tracks:
        media_id = search_plex_for_media(track_name, artist_name)
        if not media_id:
            track_url = get_spotify_track_url(access_token, track_name, artist_name)
            if track_url:
                missing_tracks.append(track_url)

    # 3. Use the command to download the missing track
    for track_url in missing_tracks:
        command = [".\\d-fi.exe", "-q", "320", "-u", track_url, "-d", "-conf", "config.json"]
        subprocess.run(command)

    # 4. Trigger Plex API to rescan the media library
    plex.library.section('Music').update()  # Replace 'Music' if your library has a different name

    # 5. Check Plex again for all tracks and create the playlists
    for playlist_url, config in playlists_data.items():
        playlist_id = playlist_url.strip().split('/')[-1]
        playlist_name, tracks = get_playlist_tracks(access_token, playlist_id)

        plex_media_ids = []
        for track_name, artist_name in tracks:
            media_id = search_plex_for_media(track_name, artist_name)
            if media_id:
                plex_media_ids.append(media_id)

        existing_playlist = get_existing_playlist(playlist_name)
        if config["override"] and existing_playlist:
            for media_id in plex_media_ids:
                media_item = plex.fetchItem(media_id)
                existing_playlist.addItems(media_item)

        else:
            counter = 1
            while existing_playlist:
                playlist_name = f"{playlist_name} {counter}"
                counter += 1
                existing_playlist = get_existing_playlist(playlist_name)
            create_plex_playlist(playlist_name, plex_media_ids)

    if missing_tracks:
        logging.info("Logging missing tracks to missing_tracks.txt")
        with open("missing_tracks.txt", "w") as missing_file:
            for track_url in missing_tracks:
                missing_file.write(track_url + "\n")



if __name__ == "__main__":
    main()
