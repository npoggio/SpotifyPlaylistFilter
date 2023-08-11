from flask import Flask, request, url_for, session, redirect, render_template, request
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import array as arr

app = Flask(__name__, static_url_path='/static')

app.config['SESSION_COOKIE_NAME'] = 'Maximum Lore'
app.config["SECRET_KEY"] = "a3sef983u2984"
TOKEN_INFO = "token-info"

# Set the redirect URI for the development environment
app.config['REDIRECT_URI'] = 'http://127.0.0.1:5000'  # Replace with your desired redirect URI

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info

    return redirect(url_for('retrieve_filter', _external=True))

@app.route('/getTracks', methods=['GET','POST'])
def retrieve_filter():
   
    try:
        token_info = session.get(TOKEN_INFO, None)
    except:
        print('User not logged in!')
        return redirect('/')
    
    # create spotify client and get all user playlists
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_playlists()
    userID = sp.current_user()['id'] 

    dropdown_items = [] 
    for playlist in results['items']:
        dropdown_items.append(playlist['name']) 

    # If the user clicked the submit button, create the playlist
    if request.method == 'POST':
        selected_playlist = request.form.get('selected_playlist')
        selected_genre = request.form.get('selected_genre')

        # get the playlist ID of the selected playlist
        playlistID = results['items'][0]['id']  
        i = 0 
        for playlist in results['items']:
            if playlist['name'] == selected_playlist:
                playlistID = results['items'][i]['id']
            i += 1
    
        # get all tracks from the playlist
        playlist = sp.playlist_items(playlistID)
        trackURIs = []

        # Create the new playlist          
        newPlaylist = sp.user_playlist_create(userID, selected_genre + " songs from " + selected_playlist , False, False, "Python generated playlist")

        # Iterate through all tracks in the playlist
        for track in playlist['items']:

            
            # get the track ID from the list
            trackID = track['track']['id']
            track2 = sp.track(trackID)

            #gets the artist of the track 
            artistID = track2['artists'][0]['id']
            artist = sp.artist(artistID)

            # gets the genre list of the artists
            genres = artist['genres']

            # check if any of the listed genres for the song has the one we are searching for
            for genre in genres:
                
                # uses user input from html form to search by genre
                if selected_genre in str(genre):
                    trackURIs.append(track['track']['uri'])
                    break
        
        display_added_tracks(trackURIs)

        # Adds all the songs that fit the genre into the new playlist
        sp.user_playlist_add_tracks(userID, newPlaylist['id'], trackURIs)
        
        # go back to the homescreen
        return redirect(url_for('retrieve_filter'))
    else:
        # set the template for the homescreen
        return render_template('index.html', dropdown_items=dropdown_items)
            
def display_added_tracks(trackURIs):

    try:
        token_info = session.get(TOKEN_INFO, None)
    except:
        print('User not logged in!')
        return redirect('/')
    
    # create spotify client and get all user playlists
    sp = spotipy.Spotify(auth=token_info['access_token'])

    for trackURI in trackURIs:   
        track = sp.track(trackURI)
        print(track['preview_url'])
    return None


def get_token():
    token_info = session.get(TOKEN_INFO, None)   
    if not token_info:
        redirect(url_for('login', _external=False))
    now = int(time.time())

    is_expired = token_info['expires at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return  SpotifyOAuth(
        client_id = "806bbd89333e439f8631cfd401c1c012",
        client_secret = "427f494d009743a2abac0f74dfd195bf",
        redirect_uri = url_for('redirectPage', _external=True),
        scope = "user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private"
    )