from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,request, session
from flask_admin import Admin
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
#from flask_login import LoginManager

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)

#login_manager = LoginManager() 
#login_manager.init_app(app) # from login documentation

# Handles all migrations.
migrate = Migrate(app, db)
babel = Babel(app, locale_selector=get_locale)
admin = Admin(app,template_mode='bootstrap4')
crsf = CSRFProtect(app)

from app import views, models

