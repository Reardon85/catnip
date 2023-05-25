# Standard library imports

# Remote library imports
import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, desc, asc, CheckConstraint, or_, and_, not_

# Local imports

# Instantiate app, set attributes
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
            )
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['AUTH0_DOMAIN'] = 'YOUR_AUTH0_DOMAIN'
app.config['AUTH0_CLIENT_ID'] = 'YOUR_AUTH0_CLIENT_ID'
app.config['AUTH0_CLIENT_SECRET'] = 'YOUR_AUTH0_CLIENT_SECRET'
app.config['AUTH0_CALLBACK_URL'] = 'YOUR_AUTH0_CALLBACK_URL'

app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)
bcrypt = Bcrypt(app)

# Instantiate CORS
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})


oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    api_base_url=f"https://{app.config['AUTH0_DOMAIN']}",
    access_token_url=f"https://{app.config['AUTH0_DOMAIN']}/oauth/token",
    authorize_url=f"https://{app.config['AUTH0_DOMAIN']}/authorize",
    client_kwargs={
        'scope': 'openid profile email',
    },
)