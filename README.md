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

# Guide to Setting Up Spotify Developer Account and Obtaining a Plex Token

## Creating a Spotify Developer Account:

1. **Navigate to the Spotify Developer Dashboard**
   - Visit the Spotify Developer Dashboard at [https://developer.spotify.com/dashboard/](https://developer.spotify.com/dashboard/)

2. **Log in or Sign Up**
   - If you already have a Spotify account, click on `Log In`.
   - If you don't have an account, click on `Sign Up` and follow the prompts to create a new Spotify account.

3. **Accept the Developer Terms of Service**
   - Once logged in, you will be prompted to agree to the Spotify Developer Terms of Service. Click `Agree` to continue.

4. **Create an App**
   - Click on the `Create an App` button.
   - Fill in the required details for your app, such as the App Name and App Description.
   - Click on `Create` once you've filled out the details.

5. **Obtain your Credentials**
   - Once your app is created, you'll be redirected to the app's dashboard. Here, you will see your `Client ID` and `Client Secret`.
   - Make note of these values; you'll need them to authenticate with the Spotify Web API.

6. **Set Redirect URIs (Optional)**
   - If you plan on using Spotify's Authorization Code Flow, you will need to set a Redirect URI.
   - In the app settings, find the `Redirect URIs` section and add your redirect URI.
   - Remember to save your settings.

Now, your Spotify Developer account is set up, and you have an app that can be used to authenticate with the Spotify API!

## Obtaining a Plex Token:

1. **Sign in to Plex**
   - Visit [Plex](https://www.plex.tv/) and make sure you're logged in.

2. **Go to a Plex Server**
   - Access any of your Plex Media Servers.

3. **Access a Media Item**
   - Go to any library (e.g., Movies, TV Shows) and click on any item.

4. **View XML Data**
   - Once viewing the details of that media item, right-click on the three-dot menu (usually at the top right) and select `Get Info`.
   - From the window that appears, click on `View XML`.

5. **Find the Plex Token**
   - In the browser's address bar, you'll see a URL that looks something like this:
     ```
     https://app.plex.tv/desktop#!/server/[server_id]/details?key=/library/metadata/[item_id]&X-Plex-Token=YOUR_PLEX_TOKEN
     ```
   - Copy the value after `X-Plex-Token=`; this is your Plex token.

6. **Store Securely**
   - Ensure that you keep this token secure. Do not share it or expose it unnecessarily, as it provides access to your Plex server.

You now have your Plex Token! Remember to integrate it safely into your scripts or applications.

**Note:** Plex tokens can expire or be revoked. If your script or app stops working, ensure the token is still valid. Always ensure you follow best security practices when handling and storing tokens.


## Notes:
Ensure you have permission to download and distribute music tracks.
The Spotify credentials used in this script are placeholders and should be replaced by actual credentials.
Ensure you modify the library name in plex.library.section('Music').update() if your Plex library has a different name.
