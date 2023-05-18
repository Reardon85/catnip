from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta
from sqlalchemy.orm import validates
from config import db, bcrypt, CheckConstraint, or_

# Models go here!




class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_pic_url = db.Column(db.String)
    bio = db.Column(db.String)

