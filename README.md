# spotify-to-plex
A script to synchronize Spotify playlists with a Plex Media Server.

## Features:
- Fetches playlists from Spotify using their API.
- Searches for those songs on a local Plex Media Server.
- If songs from Spotify playlists are not found on Plex, they can be downloaded using an external command line tool.
- Updates Plex playlists based on Spotify playlists.
- Creates logs of missing tracks.

## Requirements:
- Plex Media Server setup and running.
- Spotify Developer Account to access Spotify Web API.
- `playlists.json` file with Spotify playlist URLs and configuration.

## Usage:

1. Clone the repository.
2. Install necessary dependencies using:
    ```bash
    pip install -r requirements.txt
    ```
3. Update the script with your Spotify and Plex credentials.
4. Prepare `playlists.json` with your Spotify playlist URLs.
5. Run the script:
    ```bash
    python script_name.py
    ```

## `playlists.json` Format:
The file should contain a JSON dictionary where keys are Spotify playlist URLs and values are configuration settings. Example:
```json
{
    "https://open.spotify.com/playlist/xxxxxxx": {
        "override": true
    },
    "https://open.spotify.com/playlist/yyyyyyy": {
        "override": false
    }
}
```

## Notes:
Ensure you have permission to download and distribute music tracks.
The Spotify credentials used in this script are placeholders and should be replaced by actual credentials.
Ensure you modify the library name in plex.library.section('Music').update() if your Plex library has a different name.
