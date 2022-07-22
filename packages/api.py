import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import re 
import spotipy.util as util


client_id = '4379e8dc929f4f3d8b296962fb549d56'
client_secret= '08a15f73be3742f18227aec6fb9e61b4'
scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
        
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)
token = util.prompt_for_user_token(scope, client_id= client_id, client_secret=client_secret, redirect_uri='https://mysongrecommender/dashboard/')
sp = spotipy.Spotify(auth=token)

def uri_to_features(uri):

    
    #Audio features
    features = sp.audio_features(uri)[0]
    
    #Artist of the track, for genres and popularity
    artist = sp.track(uri)["artists"][0]["id"]
    artist_pop = sp.artist(artist)["popularity"]
    artist_genres = sp.artist(artist)["genres"]
    
    #Track popularity
    track_pop = sp.track(uri)["popularity"]
    
    #Add in extra features
    features["artist_pop"] = artist_pop
    if artist_genres:
        features["genres"] = " ".join([re.sub(' ','_',i) for i in artist_genres])
    else:
        features["genres"] = "unknown"
    features["track_pop"] = track_pop
    
    return features

if __name__ == "__main__":
    # Debug
    result = uri_to_features("1o0nAjgZwMDK9TI4TTUSNn")
    print(result)