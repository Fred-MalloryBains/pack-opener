from app import db
from flask_sqlalchemy import SQLAlchemy


class Users (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(50))
    credits = db.Column(db.Integer, default=3000000)
    spotify_connected = db.Column(db.Boolean, default=False)
    spotify_access_token = db.Column(db.String(400), nullable = True)
    spotify_refresh_token = db.Column(db.String(400), nullable = True)
    
    def __repr__(self):
        return '{}{}{}'.format(self.id, self.username, self.password)
    def check_email(self):
        if (len(self.email) < 5):
            return False
        elif (self.email.find("@") == -1):
            return False
        else:
            return True
    def check_username(self):
        if (len(self.username) < 5):
            return False
        else:
            return True
    def check_password(self):
        if (len(self.password) < 8):
            return False
        elif (self.lower() == self.password or self.upper() == self.password):
            return False
        else:
            return True


class Cards (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column (db.String(50), index = True, unique = True)
    popularity = db.Column (db.Integer)
    image_url = db.Column (db.String(400))
    genre = db.Column (db.String(20))
    uri = db.Column (db.String (400))
    rarity = db.Column (db.String(20))

class UserCards (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable = False)
    quantity = db.Column(db.Integer)
    

    
class UserPacks (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    packId = db.Column(db.String(20), db.ForeignKey('pack.id'), nullable = False)
    quantity = db.Column(db.Integer)

class Pack (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(20))
    rarity = db.Column(db.String(20))
    cost = db.Column(db.Integer)

    