from app import app, db , models
from app.models import Cards  # Import your Cards model
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Set up the Spotify API client
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
    )
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def get_top_artists(genre, limit = 50):
    top_artists = []
    offset = 0
    while len(top_artists) < limit:
        q = f'genre:"{genre}"'
        results = sp.search(q=q, limit = 50, offset=offset, type='artist', market = "US")
        artists = results['artists']['items'] 
        
        if len(artists) == 0 or offset >= results['artists']['total']:
            print ('no artists for ', genre)
            break
        
        top_artists.extend(artists)
        offset += 50
        
        
    return top_artists[:limit]


genres = ["hip hop", "jazz", "funk", "house"]
with app.app_context():
    for genre in genres:
        artist_list = get_top_artists(genre)
        print ("artists in ", genre , "\n")
        for artist in artist_list[genre]:
            new_card = Cards(
                artist_name = artist['name'],
                popularity = artist['popularity'],
                image_url = artist['images'][0]['url'] if artist['images'] else None,
                genre = genre,
                uri = artist['uri'],
            )
            db.session.add(new_card)
    db.session.commit()
print ("done")
    
        

#top_1000_artists = get_top_artists('hip hop', '1990-')
##for artist in top_1000_artists:
    
    #print(artist['name'],  artist['popularity'], artist['genres'], "\n")