Overview
=
- This Python project utilizes Flask and Spotify's API to create a web interface allowing users to filter their existing playlists based on genre and create new playlists. - 
- The application uses the SpotifyOAuth for authentication and playlist manipulation.

Setup
=
- Clone the repository.
- If you would like, replace the client_id and client_secret in the create_spotify_oauth function with your own Spotify Developer credentials.

Usage
=
- Navigate to the repository in your terminal.
- Create a virtual environment with the command .venv\Scripts\activate
- Set the FLASK_APP environmental variable by running the command `set FLASK_APP=main.py`
- Run `flask main.py`
- Open your browser and navigate to `http://127.0.0.1:5000/`.
- Log in with your Spotify credentials to authorize the application.
- The web interface will display a list of your playlists. Select a playlist and choose a genre to filter.
- Click the submit button to create a new playlist with tracks matching the selected genre.
- Check your spotify account online or on the app for your new playlist.

Dependencies
=
- Flask
- Spotipy

Configuration
=
- client_id: Your Spotify Developer client ID.
- client_secret: Your Spotify Developer client secret.
- redirect_uri: Your desired redirect URI for Spotify authentication. 

Note
=
- Ensure that your Spotify Developer account is properly configured, and the necessary scopes are granted for playlist manipulation.
- Accounts can be created here: https://developer.spotify.com/documentation/web-api
