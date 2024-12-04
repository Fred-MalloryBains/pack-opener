from app import app
from flask import render_template, flash, redirect, url_for, request, Flask, jsonify, session
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView

from .models import Users, Cards, UserCards, UserPacks, Pack
from .forms import LoginForm, RegisterForm

from dotenv import load_dotenv
# import spotipy, a pythong library for the Spotify Web API
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

#python tools
import random
import json
import os

## get client credentials from .env file
load_dotenv()
# get spotify credentials from the environment
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
scope = os.getenv('SPOTIFY_SCOPE')
app.secret_key = os.getenv('SECRET_KEY')

## create authorisation details for spotify client
cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope= scope,
    cache_handler=cache_handler,
    show_dialog=True
)

## create spotify client variable
sp = spotipy.Spotify(auth_manager=sp_oauth)
## model view in flask admin
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Cards, db.session))
admin.add_view(ModelView(Pack, db.session))
admin.add_view(ModelView(UserCards, db.session))
admin.add_view(ModelView(UserPacks, db.session))


@app.route('/')
def index():
    ## homepage 
    ## explanation of the app
    ## login page 
    ## register page
    
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None or user.password != form.password.data:
                flash('Invalid username or password')
                return redirect(url_for('login'))
            session['userId'] = user.id ##create session id
            print ("session id added , ", session['userId'])
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():    
    ## register page
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = Users(
            
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        ## validation checks from model
        if (new_user.check_email() == False):
            flash ('Invalid email')
            return redirect(url_for('register'))
        elif (new_user.check_username() == False):
            flash ('Invalid username')
            return redirect(url_for('register'))
        elif (new_user.check_password() == False):
            flash ('Invalid password')
            return redirect(url_for('register'))
        else:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("register.html", form = form)

@app.route('/link_spotify')
def link_spotify():
    ## link spotify page
    print (sp_oauth.redirect_uri)
    auth_url = sp_oauth.get_authorize_url()
    
    return redirect(auth_url)

@app.route('/callback')
def callback():
    ## spotify callback
    code = request.args.get('code')
    print(f"Authorization code received: {code}")
    try:
        token_info = sp_oauth.get_access_token(code)
        print(f"Token info: {token_info}")
    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"Error retrieving access token: {e}")
        return f"Error: {e}"
    
    session['token_info'] = token_info
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout ():
    ## clear session details
    session.clear()
    ## restart application
    return redirect(url_for('index'))

@app.route('/add_pack', methods = ['POST', 'GET'])
def add_pack():
    print (session['userId'] )
    data = request.get_json()
    packId = data['packId']
    packCredits = Pack.query.filter_by(id = packId).first().cost
    userCredits = Users.query.filter_by(id = session['userId']).first().credits
    ## can user afford pack
    if userCredits >= packCredits:
        if (UserPacks.query.filter_by(user_id = session['userId'], packId = packId).first()):
            ## old pack for user
            user_pack = UserPacks.query.filter_by(user_id = session['userId'], packId = packId).first()
            user_pack.quantity += 1
            Users.query.filter_by(id = session['userId']).first().credits -= packCredits
        else:
            ## new pack for user
            user_pack = UserPacks(
                user_id = session['userId'],
                packId = packId,
                quantity = 1
            )
            db.session.add(user_pack)
        db.session.commit()
    else:
        ## return to dashboard
        flash ('Not enough credits')
        return redirect(url_for('dashboard'))
    packs = UserPacks.query.filter_by(user_id = session['userId']).all()
    user_packs = []
    for pack in packs:
        ## create pack details 
        Id = pack.packId
        info = Pack.query.filter_by(id = Id).first()
        pack = {
            'name' : info.genre + ' ' + info.rarity + ' pack',
            'quantity' : pack.quantity,
            'id' : Id
        }
        user_packs.append(pack)
    ## return to json file to update page
    return json.dumps(user_packs)


@app.route('/dashboard')
def dashboard():
    ## dashboard page 
    ## show cards 
    ## link to store
    ## show unopened packs
    packs = Pack.query.limit(5).all()
    store_packs = []
    for packs in packs:
        pack_info = {
            'name' : packs.genre + ' ' + packs.rarity + ' pack',
            'price' : packs.cost,
            'Id' : packs.id
        }
        
        store_packs.append(pack_info)
    
    return render_template('dashboard.html', store_packs = store_packs)


@app.route('/profile')
def profile():
    
    ## profile page
    ## show cards 
    if session['userId']:
        
        spotify_linked = True
        token_info = session.get('token_info', None)
        if not token_info:
            spotify_linked = False
        userpacks = len(UserPacks.query.filter_by(user_id = session['userId']).all())
        userCards = len(UserCards.query.filter_by(user_id = session['userId']).all())
        user = Users.query.filter_by(id = session['userId']).first()
        user_info = {
            'username' : user.username,
            'email' : user.email,
            'credits' : user.credits,
            'no_of_packs' : userpacks,
            'no_of_cards' : userCards,
            'spotify_linked' : spotify_linked
        }
        return render_template('profile.html', user = user_info)
    else:
        return render_template('home.html')

def get_rarity(popularity):
    if popularity > 90:
        return 'legendary'
    elif popularity > 80:
        return 'epic'
    elif popularity > 70:
        return 'rare'
    else:
        return 'common'

@app.route('/my_cards')
def my_cards():
    ## my cards page
    ## show cards 
    token_info = session.get('token_info', None)
    if not token_info:
        flash ('please log into spotify to view card library!')
        return redirect(url_for('link_spotify'))
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
        
    # create artist list and pass into html to display cards 
    # also check db for cards
    ## create db 
    return render_template('my_cards.html')

@app.route('/my_cards_query', methods = ['POST'])
def my_cards_query():
    data = request.get_json()
    user_cards = []
    print (data)
    if data['isCollected']:
        user_cards = []
        artists = UserCards.query.filter_by(user_id = session['userId']).all()
        for artist in artists:
            card = Cards.query.filter_by(id = artist.card_id).first()
            if card.rarity == data['rarity'] or data['rarity'] == 'all':
                card_info = {
                    'name': card.artist_name,
                    'rarity': card.rarity,
                    'rarity_class' : card.rarity + '-card',
                    'image_url': card.image_url,
                    'genre': card.genre,
                }
                user_cards.append(card_info)  
              
    else:
        print ("hello")
        token_info = session.get('token_info', None)
        if not token_info:
            return redirect(url_for('link_spotify'))
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info

        sp = spotipy.Spotify(auth=token_info['access_token'])
        artist_list = []
        artists = sp.current_user_followed_artists(limit=20)
        ## keep querying until we have 100 artists or run out of artists
        ## add filters for rarity/ collected
        while artists['artists']['next'] and len(artist_list) < 100:
            artists = sp.current_user_followed_artists(limit=20, after=artists['artists']['cursors']['after'])
            for artist in artists['artists']['items']:
                rarity = get_rarity(artist['popularity'])
                artist_info = {
                    'name': artist['name'],
                    'rarity': rarity,
                    'rarity_class' : rarity + '-card',
                    'image_url': artist['images'][0]['url'] if artist['images'] else None,
                    'genre': artist['genres'][0] if artist['genres'] else None,
                }
                artist_list.append(artist_info)
                if len(artist_list) >= 100:
                    break
        for artist in artist_list:
            if artist['rarity'] == data['rarity'] or data['rarity'] == 'all':
                user_cards.append(artist)
                
    return json.dumps(user_cards)

@app.route('/open_my_packs')
def open_my_packs():
    packs = UserPacks.query.filter_by(user_id = session['userId']).all()
    user_packs = []
    for pack in packs:
        Id = pack.packId
        info = Pack.query.filter_by(id = Id).first()
        pack = {
            'name' : info.genre + ' ' + info.rarity + ' pack',
            'quantity' : pack.quantity,
            'id' : Id
        }
        user_packs.append(pack)
    return render_template('open_my_packs.html', user_packs = user_packs)

@app.route('/open-pack/', methods=['GET','POST'])
def open_pack():
    packId = request.args.get('packId')
    print (packId)
    pack_info = Pack.query.filter_by(id = packId).first()
    pack_info = {
        'name' : pack_info.genre + ' ' + pack_info.rarity + ' pack',
        'id' : pack_info.id,
    }
    
    return render_template('pack.html', pack = pack_info)
    
@app.route('/open_pack_response', methods=['GET','POST'])
def open_pack_response():
    data = request.get_json ()
    pack_info = Pack.query.filter_by(id = data['packId']).first()
    ## SOME CODE
    packed_cards = []
    while len(packed_cards) < 3:
        chosen = random.randint(1,100)
        if chosen < 65:
            rarity = 'common'
        elif chosen < 85:
            rarity = 'rare'
        elif chosen < 95:
            rarity = 'epic'
        else:
            rarity = 'legendary'
        print ("db query", rarity, pack_info.genre)
        card_list_filter = Cards.query.filter_by(rarity = rarity, genre = pack_info.genre).all()
        print ("card list", card_list_filter)
        if len(card_list_filter) > 0:
            card = random.choice(card_list_filter)
        else:
            print ("options: ",Cards.query.filter_by(genre = pack_info.genre).all())
            card = random.choice(Cards.query.filter_by(genre = pack_info.genre).all())
        card = {
            'name': card.artist_name,
            'rarity': card.rarity,
            'rarity_class': card.rarity + '-card',
            'image_url': card.image_url,
            'genre': card.genre,
        }
        packed_cards.append(card)
        card_item = Cards.query.filter_by(artist_name = card['name']).first()
        if UserCards.query.filter_by(user_id = session['userId'], card_id = card_item.id).first():
            user_card = UserCards.query.filter_by(user_id = 1, card_id = card_item.id).first()
            user_card.quantity += 1
            
        else:
            user_card = UserCards(
                user_id = session['userId'],
                card_id = card_item.id,
                quantity = 1
            )
            db.session.add(user_card)
        UserPacks.query.filter_by(user_id = session['userId'], packId = pack_info.id).first().quantity -= 1
        db.session.commit()
    ## END SOME CODE
    return json.dumps(packed_cards)