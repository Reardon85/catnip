#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from functools import wraps
from jose import jwt
import json
from flask import request, make_response, abort, jsonify, render_template, session    
from flask_restful import Resource
import os
from uuid import uuid4
import boto3
from dotenv import load_dotenv
load_dotenv()
import requests
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
from random import randint, choice as rc
from flask_socketio import SocketIO, emit, join_room



# Local imports
from config import app, db, api, auth0, or_, and_, not_, desc
from models import User, Visitor, Match, Photo, Pet, PetPhoto, Conversation, Message, favorites

# Views go here!

AUTH0_DOMAIN = "dev-yxel2dejc2kr1a0k.us.auth0.com"
API_AUDIENCE = 'https://dev-yxel2dejc2kr1a0k.us.auth0.com/api/v2/'
ALGORITHMS = ["RS256"]

app.config['SECRET_KEY'] = 'secret!'

# socketio = SocketIO(app, cors_allowed_origins="*")



# @socketio.on('join')
# def on_join(data):
#     username = session['user_id']
#     room = data
#     print(room)
#     print("You are joining the room")
#     join_room(room)
    



# @socketio.on('send_message')
# def handle_message(data):
#     sender = User.query.filter_by(id=session['user_id']).first()
    
#     room = data['convoId']
#     message = data['message']
#     print('message', message)
#     print(room)
#     emit('receive_message', {'convo_id': room, 'text': message, 'avatar_url':sender.avatar_url, 'username':sender.username}, room=room)

# @socketio.on('connect')
# def handle_connect():
#     # Perform necessary operations when a client connects
#     join_room('user_room')  # Join a room specific to the user



app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print("I am connecting and joining the room sid")
    
    join_room(request.sid)

@socketio.on('start')
def handle_listeners(data):
    the_client = User.query.filter_by(id=data['userId']).first()
    the_client.sid = request.sid
    db.session.add(the_client)
    db.session.commit()

    print("I am setting up listeners for everything")
    the_client = User.query.filter_by(id=data['userId']).first()
    fav_users = the_client.favorited_users
    #id will track fav_users. follow all channels of your favorites users
    for user in fav_users:
        print(user)
        join_room(user.id)
    
    #username will track Match / Sid will track message(maybe change later to email)
    join_room(the_client.username)
    join_room(request.sid)
    #now we got to emit to our userid so those who favorited us see we are online
    emit('favorites', {
    "avatar_url": the_client.avatar_url,
    "id": the_client.id,
    "username": the_client.username
  }, room= the_client.id)
@socketio.on('join')


def on_join(data):
    room = data['convoId']
    join_room(room)
    
    emit('user_connected', {'message':  "has entered the room."}, room=room)

@socketio.on('message')
def handle_message(data):

    the_client = User.query.filter_by(id=data['userId']).first()
    print(1)
    print(request.sid)
   
    message = Message(text=data['message'], convo_id=data['convoId'], user_id=data['userId'])
    db.session.add(message)
    print(3)
    db.session.commit()
    the_convo = message.conversation
    print(data['userId'])
    print(the_convo.user_one_id)
    print(the_convo.user_two_id)
    if int(data['userId']) == the_convo.user_one_id:
        print('inside the if ')
        the_convo.user_two_seen = False
        other_user = the_convo.user_two_id
    else:
        the_convo.user_one_seen = False

        other_user = the_convo.user_one_id
    print(other_user)
    the_user = User.query.filter_by(id = other_user).first()
    print('sid', type(the_user.sid))
    print(type(request.sid))
    for room in socketio.server.rooms(request.sid):
        print(type(room), room)
        

    print('all the rooms!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    db.session.add(the_convo)
    db.session.commit()
    print(the_user.sid)
    emit('message', {'text': data['message'], 'user_id':the_client.id, 'username':the_client.username, 'avatar_url':the_client.avatar_url, 'convoId':data['convoId'], 'created_at':the_convo.created_at.isoformat() }, room=data['convoId'])
    if the_user.sid:
        emit('msgNotify', {'username':the_client.username, 'avatar_url':the_client.avatar_url }, room=the_user.sid)






    
    




class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    """Obtains the access token from the Authorization Header"""
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the access token is valid"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = requests.get('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
        jwks = jsonurl.json()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e'],
                    'alg': key['alg']
                }
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)
        
        return f(*args, **kwargs)

    return decorated

def add_coordinates(zip_code, the_client):
    api_key = os.environ.get('GEO_CODING_KEY')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(zip_code)
    coordinates = data['results'][0]['geometry']['location']
    components = data['results'][0]['address_components']

    for component in components:
        if 'locality' in component['types']:
            city = component['long_name']
            the_client.city= city
        if 'administrative_area_level_1' in component['types']:
            state = component['short_name']

    the_client.latitude = coordinates['lat']
    the_client.longitude= coordinates['lng']
    
    the_client.state=state
    the_client.zipcode=zip_code
    db.session.add(the_client)
    db.session.commit()

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 3958.8 

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return int(distance)


class Login(Resource):
    @requires_auth
    def get(self):
        # Returns User Info for Client. May be weird Auth0. 
        # For Login component - [Insert Button Click Function]

        


        print("It worked")
        token = get_token_auth_header()
        unverified_claims = jwt.get_unverified_claims(token)
        sub_id = unverified_claims['sub']
        session['sub'] = sub_id
        the_client = User.query.filter_by(auth_sub=sub_id).first()
        if the_client:
            session['user_id'] = the_client.id
            return make_response({'newUser':False, 'user':the_client.to_dict()}, 200)
            
        return make_response({'user':False, 'newUser':True}, 200)
api.add_resource(Login, '/api/login')


class Register(Resource):
    def post(self):
        # Returns User Info for Client. May be weird Auth0. 
        # For Login component - [Insert Button Click Function]
        print("registering")
        
        file = request.files['image']
        username = request.values['username']
        email = request.values['email']
        zipcode = request.values['zipcode']
        gender = request.values['gender']
        orientation = request.values['orientation']
        birthday_str = request.values['birthday']
        birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        print (birthday)

        

        s3 = boto3.resource('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        bucket = s3.Bucket('the-tea')
        test = bucket.put_object(Key=file.filename, Body=file)
        file_url = f"https://{bucket.name}.s3.amazonaws.com/{file.filename}"

        the_client = User(
            username=username.capitalize(), 
            birthdate=birthday, 
            email=email, 
            avatar_url=file_url, 
            zipcode=zipcode, 
            orientation=orientation, 
            gender=gender, 
            auth_sub=session['sub']
            )
        first_photo = Photo(image_url=file_url, user_id=the_client.id, description="Profile Photo")
        db.session.add(the_client)
        db.session.add(first_photo)
        db.session.commit()
        first_photo = Photo(image_url=file_url, user_id=the_client.id, description="Profile Photo")
        db.session.add(first_photo)
        db.session.commit()
        session['user_id'] = the_client.id
        add_coordinates(zipcode, the_client)
        
        return make_response({'user':the_client.to_dict(), 'newUser': False}, 200)
api.add_resource(Register, '/api/register')


        











class Visited(Resource):
    def get(self):
        #Returns last 5 users the client visited, based on last_vist in Visitor obj. 
        # For Home/RecentVisits comp - useEffect[]
        the_client = User.query.filter_by(id=session['user_id']).first()
        visited_list = Visitor.query.filter_by(visitor_id=session['user_id']).limit(5).all()

        visited_dict = [{**visited.to_dict(rules=('-seen',)), **visited.visited.to_dict(only=('avatar_url', 'username'))} for visited in visited_list]

        return make_response(visited_dict, 200)
api.add_resource(Visited, '/api/visited')

class Favorites(Resource):
    def get(self):
        # Using User.favorited_users  returns a list of clients favorite users who are online . 
        # For Home/ActiveFavorites comp - useEffect[]
        the_client = User.query.filter_by(id=session['user_id']).first()
        favorites_list = [favorite.to_dict(only=('id', 'username', 'avatar_url')) for favorite in the_client.favorited_users if favorite.active_recently]
        
        return make_response(favorites_list, 200)
    def post(self):
        #Creates a Favorite obj attached to clients id and another user. User.favorited_users.append(User)
        # For Profile Component - handleAddFavorite()
        data = request.get_json()
        the_client = User.query.filter_by(id=session['user_id']).first()
        favorite_user = User.query.filter_by(id=data['userId']).first()
        the_client.favorited_users.append(favorite_user)
        db.session.commit()
        return make_response(favorite_user.to_dict(only=('username', 'id')), 201)
        
    def delete(self):
        #Deletes Favorite Obj connected to client. User.favorited_users.pop(User)
        # For Profile Component  - handleRemoveFavorite()
        data = request.get_json()
        the_client = User.query.filter_by(id=session['user_id']).first()
        favorite_user = User.query.filter_by(id=data['userId']).first()
        the_client.favorited_users.remove(favorite_user)
        db.session.commit()
        
        return make_response({'message': 'success'}, 204)
api.add_resource(Favorites, '/api/favorites')

class Suggest_Matches(Resource):
    def get(self):
        #Returns a list of 5 users who match well with the client
        # For Home/SuggestedMatches Component - useEffect[]
        the_client = User.query.filter_by(id=session['user_id']).first()
        

        gender = the_client.gender
        orientation = the_client.orientation

        # Checking Orientation and gender. I'm gonna need a better way to do this. 
        if (gender == 'Male' and orientation == 'Straight') or (gender == 'Female' and orientation == 'Gay'):
            interested_in = 'Female'
        elif (gender == 'Male' and orientation == 'Gay') or (gender == 'Female' and orientation == 'Straight'):
            interested_in = 'Male'
        else:
            interested_in = 'Other'


        # Get the ids of the users that current user has already liked or disliked.
        already_responded_users = Match.query.with_entities(Match.user_two_id).filter(
            and_(Match.user_one_id == the_client.id, Match.user_one_liked!= None)
        ).union(
            Match.query.with_entities(Match.user_one_id).filter(
            and_(Match.user_two_id ==the_client.id, Match.user_two_liked!= None)
            )
        )

        # Get the users who are not in the list of already responded users.
        suggested_matches = User.query.filter(User.id.notin_(already_responded_users)).filter(User.id != session['user_id']).filter_by(gender= interested_in).limit(5).all()
        
        if suggested_matches:
            suggested_list = [user.to_dict(only=('username', 'id', 'avatar_url')) for user in suggested_matches]
            return make_response(suggested_list, 200)
        return make_response({'error':'Not Found'}, 404)
api.add_resource(Suggest_Matches, '/api/suggested-matches')


class User_Profiles(Resource):
    def get(self, user_id):
        #Returns User Basic info for Profile and Boolean value of True if it's the clients own profile. False otherwise 
        # For Profile & Settings Comp - useEffect[]
        #If not Your profile it creates or updates Visitor obj
        the_user = User.query.filter_by(id=user_id).first()
        the_client = User.query.filter_by(id=session['user_id']).first()
        my_profile = False
        favorite_status = False
        liked = 'none'
        

        if not the_user:
            return make_response({'error':"Not Found"}, 404)

        the_client.update_activity()
        db.session.add(the_client)
        db.session.commit()

        if user_id == session['user_id']:
            my_profile = True
            
            

        else:
            if [True for status in the_client.favorited_users if the_user.id == status.id  ]:
                favorite_status = True
            print(favorite_status)
            new_visitor = Visitor.query.filter_by(user_id=user_id).filter_by(visitor_id=session['user_id']).first()
            
            if user_id > the_client.id:
                the_match = [match for match in the_client.match_two if (match.user_one_id == user_id)] 
                if the_match:
                    the_match = the_match[0] 
                    if the_match.user_two_liked == True:
                        liked = True
                    elif the_match.user_two_liked == False:
                        liked = False
            else:
                the_match = [match for match in the_client.match_one if match.user_two_id == user_id]
                if the_match:
                    the_match = the_match[0] 
                    if the_match.user_one_liked == True:
                        liked = True
                    elif the_match.user_one_liked == False:
                        liked = False
            if not new_visitor:
                new_visitor = Visitor(user_id=user_id, visitor_id=session['user_id'])
            else:
                new_visitor.last_visit= datetime.utcnow()
                new_visitor.seen=False
            db.session.add(new_visitor)
            db.session.commit()

        distance = int(calculate_distance(lat1=the_user.latitude, lon1=the_user.longitude, lat2=the_client.latitude, lon2=the_client.longitude))
        profile_info = {**the_user.to_dict(rules=('-email', '-last_request', 'age', 'last_online')), 'distance':distance, 'liked':liked}
        return make_response({'profile_info': profile_info, 'my_profile':my_profile, 'favorite_status':favorite_status }, 200)
    
    def patch(self, user_id):
        #Edits clients personal User obj. Must Check if client Id matches user_id
        # For Settings Component - handleUpdateAccount()
        ########### NEED TO ADD S3 FUNCTIONALITY ############################
        data = request.values
        print(data.keys())
        the_client = User.query.filter_by(id=user_id).first()

        if request.files.get('image'):
            file = request.files['image']
            s3 = boto3.resource('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
            bucket = s3.Bucket('the-tea')
            bucket.put_object(Key=file.filename, Body=file)
            the_client.avatar_url = f"https://{bucket.name}.s3.amazonaws.com/{file.filename}"
    
        if session['user_id']:
            for attr in data.keys():
                if attr == 'zipcode':
                    add_coordinates(data[attr], the_client)
                else:
                    setattr(the_client, attr, data[attr])
            db.session.add(the_client)
            db.session.commit()
            return make_response(the_client.to_dict(), 201)
        else:
            return make_response({'error':'Unauthorized Request'}, 400)

    def delete(self, user_id):
        #Delete's the Client's Account. Must check that client id matches user_id
        # For Settings Component - handleDeleteAccount()
        
        the_client = User.query.filter_by(id=user_id).first()

        if  session['user_id']:
            user_id = session['user_id']
            db.session.query(favorites).filter_by(user_id=user_id).delete()
            db.session.query(favorites).filter_by(favorited_id=user_id).delete()
            session['user_id'] = None
            db.session.delete(the_client)
            db.session.commit()
            return make_response({'message':'Account Deleted Successfully'}, 204)
        else:
            return make_response({'error':'Unauthorized Request'})
api.add_resource(User_Profiles, '/api/user/<int:user_id>')


class User_Photos(Resource):
    def get(self, user_id):
        #Returns the 6 photos for a User with user_id. 
        #For Profile/Photos component - useEffect[]
        Photo_list = Photo.query.filter_by(user_id=user_id).limit(6).all()
        print(Photo_list)
        photo_dict_list = [photo.to_dict() for photo in Photo_list]
        return make_response(photo_dict_list, 200)
    
    def post(self, user_id):
        #Add's an Photo Obj with user_id. Must check that Client id matches user_id
        #For ImageUpload Component - handleUserImage()
        file = request.files['image']
        description = request.values['description']
        if user_id == session['user_id']:
            s3 = boto3.resource('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
            bucket = s3.Bucket('the-tea')
            bucket.put_object(Key=file.filename, Body=file)
            file_url = f"https://{bucket.name}.s3.amazonaws.com/{file.filename}"

            new_photo = Photo(user_id=user_id, description=description, image_url=file_url)
            db.session.add(new_photo)
            db.session.commit()
            return make_response({'message':'Image Uploaded Successfully'}, 201)
api.add_resource(User_Photos, '/api/user/photos/<int:user_id>')

class Remove_User_Photo(Resource):
    def delete(self, photo_id):
        #Deletes Photo obj with photo_id. Checks if Photo.user_id matches client id
        # For Profile/Photos Component - handleRemoveImage()
        photo = Photo.query.filter_by(id=photo_id).first()

        if photo and photo.user_id == session['user_id']:
            db.session.delete(photo)
            db.session.commit()
            return make_response({'message':'Photo successfully delelted'})
        return make_response({'error':'Unauthorized Action'}, 400)
api.add_resource(Remove_User_Photo, '/api/photo/<int:photo_id>')

class User_Pets(Resource):
    def get(self, user_id):
        #Returns a list of the Pets where pet.user_id is user_id
        # For User/Pets component - useEffect[]
        pet_list = Pet.query.filter_by(user_id=user_id).all()
        if pet_list:
            pet_dict_list = [pet.to_dict() for pet in pet_list]
            return make_response(pet_dict_list, 200)
        return make_response({'error':'Not Found'}, 404)

    def post(self, user_id):
        #Adds a new Pet Obj for Client where Pet.user_id is user_id. Must check that user_id matches Client id
        # FOR CreatePet component - handleAddPet()
        # THis is gonna need Image s3 Stuff ################################# !!!!!!!!!!!!!!!!!!!!!
        data = request.values
        file = request.files['image']
        s3 = boto3.resource('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        bucket = s3.Bucket('the-tea')
        bucket.put_object(Key=file.filename, Body=file)
        file_url = f"https://{bucket.name}.s3.amazonaws.com/{file.filename}"
        if user_id == session['user_id']:
            try:
                new_pet = Pet(
                    user_id=user_id, 
                    name=data['name'], 
                    avatar_url=file_url,
                    animal=data['animal'],
                    temperment=data['temperment'],
                    size=data['size'] 
                    )
                db.session.add(new_pet)
                db.session.commit()
                return make_response(new_pet.to_dict(), 201)
            except Exception as ex:
                return  make_response({'error': [ex.__str__()]}, 422)
        else:
            return make_response({'error': "Not Authorized"}, 400)
api.add_resource(User_Pets, '/api/user/pets/<int:user_id>')

class Pet_Profiles(Resource):
    def get(self, pet_id):
        #Returns basic pet Info for Pet's Profile
        # FOR PetProfile component - useEffect[]
        pet = Pet.query.filter_by(id=pet_id).first()
        return make_response(pet.to_dict(), 200)
    def patch(self, pet_id):
        #Edit Client's Pet obj with id of pet_id. Must check if pet.user_id matches client id
        # Probably WILL NOT USE. will just have you delete your pet. no componenet yet
        pass
    def delete(self, pet_id):
        #Will delete the Clients Pet Obj with id of pet_id. Must check if Pet.user_id matches client id
        # FOR PetProfile component - handleRemovePet()
        pet = Pet.query.filter_by(id=pet_id).first()
        if pet and pet.user_id == session['user_id']:
            try:
                db.session.delete(pet)
                db.session.commit()
                return make_response({'message', 'Pet Successfully Deleted'}, 200)
            except Exception as ex:
                return make_response({'error': [ex.__str__()]}, 422)
        else:
            return make_response({'error': 'Unauthorized Request'}, 400)
api.add_resource(Pet_Profiles, '/api/pet/<int:pet_id>')

class PetPhotos(Resource):
    def get(self, pet_id):
        #Return a list of Pet.photos.to_dict() (query is faster)
        # For PetProfile/Photos component - useEffect[]
        # Will need to add logic to PHotos useEffect fetch if we want to reuse component for pets and Users
        pet_photos = PetPhoto.query.filter_by(pet_id=pet_id).limit(6).all()
        if pet_photos:
            pet_photos_dict = [pet.to_dict() for pet in pet_photos]
            return make_response(pet_photos_dict, 200)
        return make_response({'error':'Not Found'}, 200)
    
    def post(self, pet_id):
        #Add's an PetPhoto Obj with pet_id. Must check that Client id matches Pet.user_id where Pet.id is pet_id
        # For ImageUpload component - handlePetImage()
        pet = Pet.query.filter_by(id=pet_id).first()
        if pet and pet.user_id == session['user_id']:
            try:
                file = request.files['image']
                description = request.values['description']
                s3 = boto3.resource('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
                bucket = s3.Bucket('the-tea')
                bucket.put_object(Key=file.filename, Body=file)
                file_url = f"https://{bucket.name}.s3.amazonaws.com/{file.filename}"
                
                new_pet_photo = PetPhoto(pet_id=pet_id, image_url=file_url, description=description)
                db.session.add(new_pet_photo)
                db.session.commit()
                return make_response({'message': 'Image Uploaded Successfully'}, 201)
            except Exception as ex:
                return make_response({'error':ex.__str__()}, 422)
        else:
            return make_response({'error': 'Unauthorized Action'}, 400)

api.add_resource(PetPhotos, '/api/pet/photos/<int:pet_id>')


class Remove_PetPhoto(Resource):
    def delete(self, petphoto_id):
        #Deletes Photo obj with petphoto_id. Must checks that PetPhoto.pet.user_id matches client id
        # For PetProfile/Photos Component - handleRemoveImage()
        pet_photo = PetPhoto.query.filter_by(id=petphoto_id).first()
        
        if pet_photo and pet_photo.pet.user_id == session['user_id']:
            try:
                db.session.delete(pet_photo)
                db.session.commit()
                return make_response({'message':'Image Successfully Deleted'}, 204)
            except Exception as ex:
                return make_response({'error': ex.__str__()}, 422)
        else:
            return make_response({'error':'Unauthorized Action'}, 400)
api.add_resource(Remove_PetPhoto, '/api/petphotos/<int:petphoto_id>')


class Quick_Match(Resource):
    def get(self):
        #Returns a list of 20 profiles(user.id, avatar_url, username) that client hasn't already liked/passed on. So client to like or pass on
        # For Match/QuickMatch component - useEffect[moreMatches]

        the_client = User.query.filter_by(id=session['user_id']).first()

        gender = the_client.gender
        orientation = the_client.orientation
        preferences = the_client.interested_in.split('/')
        attribute = ['gender', 'ethnicity', 'status', 'diet', 'religion', 'orientation', 'distance', 'age_range' ]
        query = User.query

        for i in range(len(preferences)):
            
            if attribute[i] == 'age_range':
                min, max = preferences[i].split(',')
                min_age = datetime.now() -  timedelta(days= 365.25*int(min))
                max_age = datetime.now() - timedelta(days=365.25*int(max))
                query = query.filter(and_(User.birthdate <= min_age, User.birthdate >= max_age))
            elif attribute[i] == 'distance':
                
                query = query.filter(db.func.earth_distance(
                    db.func.ll_to_earth(the_client.latitude, the_client.longitude),
                    db.func.ll_to_earth(User.latitude, User.longitude)
                    ) <= (int(preferences[i])*1600))
            elif not preferences[i] == "NA":
                query = query.filter()


        # Checking Orientation and gender. I'm gonna need a better way to do this. 
        if (gender == 'Male' and orientation == 'Straight') or (gender == 'Female' and orientation == 'Gay'):
            interested_in = 'Female'
        elif (gender == 'Male' and orientation == 'Gay') or (gender == 'Female' and orientation == 'Straight'):
            interested_in = 'Male'
        else:
            interested_in = 'Other'


        # Get the ids of the users that current user has already liked or disliked.
        already_responded_users = Match.query.with_entities(Match.user_two_id).filter(
            and_(Match.user_one_id == the_client.id, Match.user_one_liked!= None)
        ).union(
            Match.query.with_entities(Match.user_one_id).filter(
            and_(Match.user_two_id ==the_client.id, Match.user_two_liked!= None)
            )
        )

        # Get the users who are not in the list of already responded users.
        potential_matches = query.filter(User.id.notin_(already_responded_users)).filter(User.id != session['user_id']).limit(15).all()


        if potential_matches:
            potential_dict_list = [suitor.to_dict(only=('username', 'id', 'avatar_url', 'photos')) for suitor in potential_matches]
            return make_response(potential_dict_list, 200)
        return make_response({'error':'Not Found'}, 200)
api.add_resource(Quick_Match, '/api/quick-match')



class Matches(Resource):
    def get(self):
        #Return all all the Users's the Client has Matched with
        # For Match/Matches component - useEffect[]
        the_client_id = session['user_id']
        match_objs = Match.query.filter(or_(Match.user_one_id==session['user_id'], Match.user_two_id==session['user_id'])).filter(Match.matched == True).all()
        user_matched_list = []
        for match in match_objs:
            if match.user_one_id == the_client_id:
                user_matched_list.append(match.user_two.to_dict(only=('username', 'avatar_url', 'id', 'photos')))
            else:
                user_matched_list.append(match.user_one.to_dict(only=('username', 'avatar_url', 'id', 'photos')))
        
        return make_response(user_matched_list, 200)

    def post(self):
        #passes user_id in Post body. Checks to see if a Match Obj already exists for the user_id and client id. If not create one and set user_one/two_liked to true.
        # For Profile &  QuickMatch component - handleJudgement()
        
        data = request.get_json()
        user_id = int(data['userId'])
        the_client_id = int(session['user_id'])
        if user_id == the_client_id:
            return make_response({'error':"Unauthorized Action"}, 400)
      
        if user_id > the_client_id:
            match_obj = Match.query.filter(Match.user_one_id==user_id).filter(Match.user_two_id==the_client_id).first()
            if not match_obj:
                match_obj = Match(user_one_id=user_id, user_two_id=the_client_id, user_two_liked=data['judgement'])
            else:
                match_obj.user_two_liked= data['judgement']
            db.session.add(match_obj)
            db.session.commit()
            match_dict = match_obj.to_dict(only=('user_one_id', 'user_two_id', 'user_one_liked'))
        else:
            match_obj = Match.query.filter(Match.user_one_id==the_client_id).filter(Match.user_two_id==user_id).first()
            if not match_obj:
                match_obj = Match(user_two_id=user_id, user_one_id=the_client_id, user_one_liked=data['judgement'])
            else:
                match_obj.user_one_liked= data['judgement']
            db.session.add(match_obj)
            db.session.commit()
            match_dict = match_obj.to_dict(only=('user_one_id', 'user_two_id', 'user_one_liked'))
        
        user_one = match_obj.user_one 
        user_two = match_obj.user_two
        compatability = match_percentage(user_one, user_two)
        print(compatability)
        emit('matched', {**match_obj.user_two.to_dict(only={'username', 'avatar_url', 'id'}), 'match_percentage': compatability }, room=match_obj.user_one.username, namespace='/')
        emit('matched', {**match_obj.user_one.to_dict(only={'username', 'avatar_url', 'id'}), 'match_percentage': compatability}, room=match_obj.user_two.username, namespace='/')
        return make_response(match_dict, 200)
     
api.add_resource(Matches, '/api/match')

class Visitors(Resource):
    def get(self):
        #Return a list of the last 20 users that visted the Client's Profile and the time they visited.
        # For Match/Visitors component = useEffect[]
        visitor_list = Visitor.query.filter_by(user_id=session['user_id']).order_by(desc(Visitor.last_visit)).limit(20).all()
     
        visitors_dict_list= []
        if visitor_list:
            for visitor in visitor_list:
                visitors_dict = {**visitor.to_dict(), **visitor.visitor.to_dict(only=('username', 'avatar_url'))}
                visitors_dict_list.append(visitors_dict)
                visitor.seen = True
                db.session.add(visitor)
                db.session.commit()
            return make_response(visitors_dict_list, 200)
        return make_response({'error':'Not Found'}, 400)
api.add_resource(Visitors, '/api/visitors')

class Conversations(Resource):
    def get(self):
        #Returns a list of all the conversations the client has had. Including the avatar_url and username of the other user ordered by most recent
        #May need to mess aroudn with websockets. 
        # For Conversation component - useEffect[]
        the_client = User.query.filter_by(id=session['user_id']).first()
        convos = the_client.conversations
        convo_list = []
        the_dict = {}

        if convos:
            first_convo_id = convos[0].id
            first_convo_mes = convos[0].to_dict(only=('messages',))
        for convo in convos:
            if convo.user_one_id == the_client.id:
                other_user = User.query.filter_by(id=convo.user_two_id).first()
                seen = {'seen': convo.user_one_seen}
            else:
                other_user = User.query.filter_by(id=convo.user_one_id).first()
                seen = {'seen': convo.user_two_seen}

            message_list = [{**message.to_dict(), **message.user.to_dict(only=('avatar_url', 'username'))} for message in convo.messages]
            the_dict[convo.id] = [{**message.to_dict(), **message.user.to_dict(only=('avatar_url', 'username'))} for message in convo.messages]
            convo_list.append({**convo.to_dict(),**seen, **other_user.to_dict(only=('avatar_url', 'username'))})
        
        return make_response({'convo_id': first_convo_id, 'messages': the_dict, 'list':convo_list}, 200)
    
    def post(self):
        #Passes user_id in post body. Check if a Converation obj for the client and user_id already exists if it does then update the updated_at time. otherwise create Obj
        # For Profile component - handleMessageUser()
        data = request.get_json()
        the_client_id = session['user_id']
        other_user_id = int(data['userId'])
    
        if the_client_id > other_user_id:
            user_one_id = the_client_id
            user_two_id = other_user_id
        elif the_client_id < other_user_id:
            user_one_id = other_user_id
            user_two_id = the_client_id
        else:
            return make_response({'error':'user_id can not be the same as client'}, 400)
        
        the_convo = Conversation.query.filter_by(user_one_id=user_one_id).filter_by(user_two_id=user_two_id).first()
        if the_convo:
            the_convo.update_timestamp()
        else:
            the_convo = Conversation(user_one_id=user_one_id, user_two_id=user_two_id)
        db.session.add(the_convo)
        db.session.commit()
        return make_response(the_convo.to_dict(), 200)

api.add_resource(Conversations, '/api/conversations')


class Messages(Resource):
    def get(self, convo_id):
        #Return all the Message obj orded by date where Message.convo_id = convo_id. Make sure that Conversation.user_one/two_id matches client's id
        # For Messages component - useEffect[]
        convo = Conversation.query.filter_by(id=convo_id).first()
        if session['user_id'] == convo.user_one_id:
            convo.user_one_seen = True
        else:
            convo.user_two_seen = True
        db.session.add(convo)
        db.session.commit()

        message_list = [{**message.to_dict(), **message.user.to_dict(only=('avatar_url', 'username'))} for message in convo.messages]
        return make_response(message_list, 200)
    
    def post(self, convo_id):
        #Creates a new Message obj for Client Convo. Make sure the client id matches the user_id for Conversation with an id of convo_id
        # For Messages component - handleSubmitMessage()
        #### Double check that you are insuring you can't post a message to a convo you arne't in
        data = request.get_json()
        the_client = User.query.filter_by(id=session['user_id']).first()
        
        try:
            message = Message(text=data['text'], convo_id=data['convoId'], user_id=session['user_id'])
            db.session.add(message)
            db.session.commit()
            the_convo = message.conversation

            if session['user_id'] == the_convo.user_one_id:
                the_convo.user_two_seen = False
            else:
                the_convo.user_one_seen = False
            db.session.add(the_convo)
            db.session.commit()
            return make_response({**message.to_dict(), **the_client.to_dict(only=('avatar_url', 'username'))}, 201)
        except Exception as ex:
            return make_response({'error':ex.__str__()}, 422) 
api.add_resource(Messages, '/api/messages/<int:convo_id>')


###### Need to Add Search Routes. 

class AdvancedSearch(Resource):
    def get(self):

        params = request.args

        the_client = User.query.filter_by(id=session['user_id']).first()

        query = User.query
        order = False
        
        for attr, value in params.items():
            if attr == 'age':
                
                min_age, max_age = map(int, value.split(','))
                min_date = datetime.now() - timedelta(days=min_age*365.25)
                max_date = datetime.now() - timedelta(days=max_age*365.25)
          
                
                query = query.filter(and_(User.birthdate<= min_date , User.birthdate>= max_date))
                
            
            elif attr == "distance":
                
                
                print(int(value)*1600)
                query = query.filter(db.func.earth_distance(
                    db.func.ll_to_earth(the_client.latitude, the_client.longitude),
                    db.func.ll_to_earth(User.latitude, User.longitude)
                    ) <= (int(value)*1600))
            elif attr=="sort":
                order=True
                order_by= value
            else: 
                query = query.filter(getattr(User,attr) == value)

        user_list = query.filter( User.id != session['user_id'] ).all()
        user_dict = [
            {
                **user.to_dict(only=('avatar_url', 'id', 'username', 'age', 'gender', 'orientation', 'last_request')), 
                'distance':calculate_distance(user.latitude, user.longitude, the_client.latitude, the_client.longitude),
                'match_percentage': match_percentage(the_client=the_client, the_user=user)
            } 
            for user in user_list]
        
        if order:
            if order_by == 'match_percentage' or order_by== 'last_request':
                user_dict = sorted(user_dict, key= lambda x:x.get(order_by), reverse=True)
            else:
                user_dict = sorted(user_dict, key= lambda x:x.get(order_by))
        
        return make_response(user_dict, 200)
api.add_resource(AdvancedSearch, '/api/search/')

def match_percentage(the_client, the_user):
    client_interested = the_client.interested_in.split('/')
    client_info = [the_client.gender, the_client.ethnicity, the_client.status, the_client.diet, the_client.religion, the_client.orientation, calculate_distance(the_user.latitude, the_user.longitude, the_client.latitude, the_client.longitude), the_client.age]
    user_interested = the_user.interested_in.split('/')
    user_info = [the_user.gender, the_user.ethnicity, the_user.status, the_user.diet, the_user.religion, the_user.orientation, calculate_distance(the_user.latitude, the_user.longitude, the_client.latitude, the_client.longitude), the_user.age]
    total_comparisons = len(client_info)*2 
    print('client intereset', client_interested)
    print('user interested', user_interested)
    match_interest = 0

    for index in range(len(client_interested)):
        # add a point if client has no preference or if their preference matches with User's info
        print(index)
        if index == 7:
            min, max = client_interested[index].split(',')
            if user_info[index] >= int(min) and user_info[index] <= int(max):
                match_interest +=1
        elif index == 6 and (int(client_interested[index]) >= user_info[index]):
            match_interest +=1
        elif client_interested[index] == "NA":
            match_interest += 1
        elif client_interested[index] == user_info[index]:
            match_interest += 1
        
        # Saving time on writing another for in loop by doing the same but with the_user's preferences
        if index == 7:
            min, max = client_interested[index].split(',')
            if user_info[index] >= int(min) and user_info[index] <= int(max):
                match_interest +=1
        elif index == 6 and (int(client_interested[index]) >= user_info[index]):
            match_interest +=1
        elif user_interested[index] == "NA":
            match_interest += 1
        elif user_interested[index] == client_info[index]:
            match_interest += 1
    print(match_interest)
    return int((match_interest/total_comparisons)*100)



# @app.route('/login')
# def login():
#     return auth0.authorize_redirect(redirect_uri=app.config['AUTH0_CALLBACK_URL'])

# @app.route('/callback')
# def callback():
#     auth0.authorize_access_token()
#     resp = auth0.get('userinfo')
#     userinfo = resp.json()
#     return jsonify(userinfo)

@app.route('/')
@app.route('/<int:id>')
def index(id=0):
    return render_template("index.html")

if __name__ == '__main__':
   
    socketio.run(app, port=5555, debug=True)
    