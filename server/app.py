#!/usr/bin/env python3

# Standard library imports

# Remote library imports

from flask import request, make_response, abort, jsonify, render_template, session    
from flask_restful import Resource
import os
from uuid import uuid4
import boto3
from dotenv import load_dotenv
load_dotenv()

# Local imports
from config import app, db, api, auth0, or_, and_, not_
from models import User, Visitor, Match, Photo, Pet, PetPhoto, Conversation, Message, favorites

# Views go here!

class Login(Resource):
    def get(self):
        # Returns User Info for Client. May be weird Auth0. 
        # For Login component - [Insert Button Click Function]
        pass

api.add_resource(Login, '/api/login')

class Check_Session(Resource):
    def get(self):
        # Might Not Need. 
        # For App Component - useEffect[]
        pass
api.add_resource(Check_Session, '/api/check-session')










class Visited(Resource):
    def get(self):
        #Returns last 5 users the client visited, based on last_vist in Visitor obj. 
        # For Home/RecentVisits comp - useEffect[]
        the_client = User.query.filter_by(id=session['user_id']).first()
        visited_list = Visitor.query.filter_by(visitor_id=session['user_id']).limit(5).all()

        visited_dict = [{**visited.to_dict(rules=('-seen')), **visited.visited.to_dict(only=('avatar_url', 'username'))} for visited in visited_list]

        return make_response(visited_dict, 200)
api.add_resource(Visited, '/api/visited')

class Favorites(Resource):
    def get(self):
        # Using User.favorites  returns a list of clients favorite users who are online . 
        # For Home/ActiveFavorites comp - useEffect[]
        the_client = User.query.filter_by(id=session['user_id']).first()
        favorites_list = [favorite.to_dict(only=('id', 'username', 'avatar_url')) for favorite in the_client.favorites if favorite.active_recently()]
        
        return make_response(favorites_list, 200)
    def post(self):
        #Creates a Favorite obj attached to clients id and another user. User.favorites.append(User)
        # For Profile Component - handleAddFavorite()
        data = request.json()
        the_client = User.query.filter_by(id=session['user_id']).first()
        favorite_user = User.query.filter_by(id=data['fav_user_id']).first()
        the_client.favorites.append(favorite_user)
        db.session.commit()
        return make_response(favorite_user.to_dict(only=('username', 'id')), 201)
        
    def delete(self):
        #Deletes Favorite Obj connected to client. User.favorites.pop(User)
        # For Profile Component  - handleRemoveFavorite()
        data = request.json()
        the_client = User.query.filter_by(id=session['user_id']).first()
        favorite_user = User.query.filter_by(id=data['fav_user_id']).first()
        the_client.favorites.remove(favorite_user)
        db.session.commit()
        return make_response({'message': 'success'}, 204)
api.add_resource(Favorites, '/api/favorites')

class Suggest_Matches(Resource):
    def get(self):
        #Returns a list of 5 users who match well with the client
        # For Home/SuggestedMatches Component - useEffect[]
        suggested_matches = User.query.filter_by(id=session['user_id']).filter(
            or_(
                not_(User.match_one.any(Match.user_one_liked==True, Match.user_one_liked==False)),
                not_(User.match_two.any(Match.user_two_liked==True, Match.user_two_liked==False))
            )
        ).limit(5).all()
        
        if suggested_matches:
            suggested_list = [user.to_dict(only=('username', 'id', 'avatar_url')) for user in suggested_matches]
            return make_response(suggested_list, 200)
        return make_response({'error':'Not Found'}, 400)
api.add_resource(Suggest_Matches, '/api/suggested-matches')


class User_Profiles(Resource):
    def get(self, user_id):
        #Returns User Basic info for Profile and Boolean value of True if it's the clients own profile. False otherwise 
        # For Profile & Settings Comp - useEffect[]
        #If not Your profile it creates or updates Visitor obj
        the_user = User.query.filter_by(id=user_id).first()
        my_profile = False

        if user_id == session['user_id']:
            my_profile = True

        profile_info = the_user.to_dict(rules=('-email', '-last_request'))
        return make_response({'profile_info': profile_info, 'my_profile':my_profile }, 200)
    
    def patch(self, user_id):
        #Edits clients personal User obj. Must Check if client Id matches user_id
        # For Settings Component - handleUpdateAccount()
        ########### NEED TO ADD S3 FUNCTIONALITY ############################
        data = request.get_json()
        the_client = User.query.filter_by(id=user_id).first()

        if user_id == session['client_id']:
            for attr in data.keys():
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

        if user_id == session['user_id']:
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
            pet_dict_list = [pet.to_dict for pet in pet_list]
            return make_response(pet_dict_list, 200)
        return make_response({'error':'Not Found'}, 404)

    def post(self, user_id):
        #Adds a new Pet Obj for Client where Pet.user_id is user_id. Must check that user_id matches Client id
        # FOR CreatePet component - handleAddPet()
        data = request.get_json()
        if user_id == session['user_id']:
            try:
                new_pet = Pet(
                    user_id=user_id, 
                    name=data['name'], 
                    avatar_url=data['avatar_url'],
                    animal=data['animal'],
                    breed=data['breed'],
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
        potential_matches = User.query.filter_by(id=session['user_id']).filter(
            or_(
                not_(User.match_one.any(Match.user_one_liked==True, Match.user_one_liked==False)),
                not_(User.match_two.any(Match.user_two_liked==True, Match.user_two_liked==False))
            )
        ).limit(20).all()
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
        match_objs = Match.query.filter(or_(Match.user_one_id==session['user_id'], Match.user_two_id==session['user_id'])).filter(Match.matched == True).limit.all()
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
        user_id = data['user_id']
        the_client_id = session['user_id']
        if user_id == the_client_id:
            return make_response({'error':"Unauthorized Action"}, 400)
        try:
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
            return make_response(match_dict, 200)
        except Exception as ex:
            return make_response({'error':ex.__str__()}, 422)
api.add_resource(Matches, '/api/match')

class Visitors(Resource):
    def get(self):
        #Return a list of the last 20 users that visted the Client's Profile and the time they visited.
        # For Match/Visitors component = useEffect[]
        visitor_list = Visitor.query.filter_by(user_id=session['user_id']).limit(20).all()
        if visitor_list:
            visitors_dict = [{**visitor.to_dict() **visitor.visitor.to_dict(only=('username', 'avatar_url'))} for visitor in visitor_list]
            return make_response(visitors_dict, 200)
        return make_response({'error':'Not Found'}, 400)
api.add_resource(Visitors, '/api/visitors')

class Conversations(Resource):
    def get(self):
        #Returns a list of all the conversations the client has had. Including the avatar_url and username of the other user ordered by most recent
        #May need to mess aroudn with websockets. 
        # For Conversation component - useEffect[]
        the_client = User.query.filter_by(id=session['user_id']).first()
        convo_list = []
        for convo in the_client.conversations:
            if convo.user_one_id == the_client.id:
                other_user = User.query.filter_by(id=convo.user_two_id).first()
                seen = {'seen': convo.user_one_seen}
            else:
                other_user = User.query.filter_by(id=convo.user_one_id).first()
                seen = {'seen': convo.user_two_seen}
            convo_list.append({**convo.to_dict(),**seen, **other_user.to_dict(only=('avatar_url', 'username'))})
        
        return make_response(convo_list, 200)
    
    def post(self):
        #Passes user_id in post body. Check if a Converation obj for the client and user_id already exists if it does then update the updated_at time. otherwise create Obj
        # For Profile component - handleMessageUser()
        data = request.get_json()
        the_client_id = session['user_id']
        other_user_id = data['user_id']
        try:
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
                the_convo.updated_timestamp()
            else:
                the_convo = Conversation(user_one_id=user_one_id, user_two_id=user_two_id)
            db.session.add(the_convo)
            db.session.commit()
            return make_response(the_convo.to_dict(), 200)
        except Exception as ex:
            return make_response({'error':ex.__str__()}, 422)
api.add_resource(Conversations, '/api/conversations')


class Messages(Resource):
    def get(self, convo_id):
        #Return all the Message obj orded by date where Message.convo_id = convo_id. Make sure that Conversation.user_one/two_id matches client's id
        # For Messages component - useEffect[]
        convo = Conversation.query.filter_by(id=id).first()
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
            message = Message(text=data['text'], converation_id=data['convoId'], user_id=session['user_id'])
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
    app.run(port=5555, debug=True)
