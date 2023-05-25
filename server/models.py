from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta
from sqlalchemy.orm import validates
from config import db, bcrypt, CheckConstraint, or_

# Models go here!


favorites = db.Table('favorites',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('favorited_id', db.Integer, db.ForeignKey('users.id'))
                     )


class Visitor(db.Model, SerializerMixin):
    __tablename__= 'visitors'

    serialize_rules=('-visitor', '-visited')

    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    visitor_id= db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, )
    seen= db.Column(db.Boolean, default=False)
    last_visit= db.Column(db.DateTime, server_default=db.func.now())


    __table_args__ = (db.UniqueConstraint('user_id', 'visitor_id', name='unique_user_visitor'), )





class Match(db.Model, SerializerMixin):
    __tablename__= 'matches'

    id = db.Column(db.Integer, primary_key=True)
    user_one_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    user_two_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    user_one_liked= db.Column(db.Boolean)
    user_two_liked= db.Column(db.Boolean)
    user_one_seen= db.Column(db.Boolean, default=False)
    user_two_seen= db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime, server_default=db.func.now())

    @hybrid_property
    def matched(self):
        return self.user_one_liked and self.user_two_liked


    


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules= ('-favorites','-favorited_by', '-visitors','-visited', '-conversations', '-messages', '-pets')
    

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    avatar_url = db.Column(db.String)
    bio = db.Column(db.String)
    last_request = db.Column(db.DateTime, default=datetime.utcnow)

    #Do I need a backref in favorites. Since a user should never know who favorited them
    #possibly to do a cascade delete, but not sure if cascadeeletes workon association tables
    favorites= db.relationship('User',
                            primaryjoin=(favorites.c.favorited_id ==id),
                            secondaryjoin=(favorites.c.user_id==id),
                            cascade="all, delete")
    
    visitors= db.relationship('Visitor',
                              foreign_keys=["Visitor.user_id"],
                              order_by="desc(Visitor.last_visit)",
                              backref='visited',
                              cascade="all, delete, delete-orphan"
                              )
    
    visited= db.relationship('Visitor',
                            foreign_keys=["Visitor.visitor_id"],
                            order_by="desc(Visitor.last_visit)",
                            backref='visitor',
                            cascade="all, delete, delete-orphan"
                            )

    # We may want to add a relationship for Matches but we will wait till we know its necessary    
    # If its possible to filter it so it'snot only matches where matched is true. it would be good. 
    conversations = db.relationship("Conversation", 
                                    primaryjoin="or_(User.id==Conversation.user_one_id, User.id==Conversation.user_two_id)",
                                    order_by="desc(Conversation.updated_at)"
                                    )
    match_one = db.relationship("Match",
                                foreign_keys=['Match.user_one_id'],
                                backref= "user_one",
                                cascade="all, delete, delete-orphan"
    )
    match_two = db.relationship("Match",
                                foreign_keys=['Match.user_two_id'],
                                backref= 'user_two',
                                cascade="all, delete, delete-orphan"
    )
    messages = db.relationship('Message', backref='user',  cascade="all, delete, delete-orphan")
    photos = db.relationship('Photo', backref='user', cascade="all, delete, delete-orphan")
    pets= db.relationship('Pet', backref='user', cascade='all, delete, delete-orphan')


    def update_activity(self):
        self.last_request= datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def logged_off(self):
        self.last_request = self.last_request + timedelta(minutes=100)
        db.session.add(self)
        db.session.commit()
    
    @hybrid_property
    def active_recently(self):
        diff = datetime.utcnow() - self.last_request

        if diff <timedelta(minutes=2):
            return True
        else:
            return False
          
    




class Photo(db.Model, SerializerMixin):
    __tablename__ = 'photos'

    serialize_rules=('-user',)

    id = db.Column(db.Integer, primary_key=True)
    image_url= db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at= db.Column(db.DateTime, server_default=db.func.now())



class Pet(db.Model, SerializerMixin):
    __tablename__ = 'pets'

    serialize_rules=('-user', '-photos')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    avatar_url = db.Column(db.String)
    animal= db.Column(db.String)
    breed= db.Column(db.String)
    temperment= db.Column(db.String)
    size= db.Column(db.String)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))

    photos = db.relationship('PetPhoto', backref='pet', cascade="all, delete, delete-orphan")



class PetPhoto(db.Model, SerializerMixin):
    __tablename__ = 'petphotos'
    serialize_rules=('-pet',)

    image_url= db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    created_at= db.Column(db.DateTime, server_default=db.func.now())


class Conversation(db.Model, SerializerMixin):
    __tablename__= 'conversations'

    serialize_rules=('-messages')

    id = db.Column(db.Integer, primary_key=True)
    user_one_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    user_two_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    user_one_seen= db.Column(db.Boolean, default=False)
    user_two_seen= db.Column(db.Boolean, default=False)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at= db.Column(db.DateTime, default=db.func.now())

    messages= db.relationship('Message', backref='conversation', cascade="all, delete, delete-orphan")

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

class Message(db.Model, SerializerMixin):
    __tablename__='messages'
    serialize_rules=('-conversation','-user')
    
    id= db.Column(db.Integer, primary_key=True)
    text= db.Column(db.String)
    convo_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at= db.Column(db.DateTime, server_default=db.func.now())




