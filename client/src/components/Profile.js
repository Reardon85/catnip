import React, {useEffect, useState} from 'react';
import './styles/app.css';
import {Link, json, useParams, useNavigate } from "react-router-dom";
import { Tab, Tabs, ListGroup, Card, Row, Col, Stack, Button, DropdownButton, Dropdown} from 'react-bootstrap';
import About from './About';
import Photos from './Photos';
import Pets from './Pets';
import PhotoCarousel from './PhotoCarousel';


const Profile = () => {
    const [profileInfo, setProfileInfo] = useState({})
    const [myProfile, setMyProfile] = useState({})
    const [liked, setLiked] = useState(null)
    const [favorited, setFavorited] = useState(null)
    const {userId} = useParams()
    const navigate = useNavigate()


    
    useEffect(() => {
        //User_Profiles - get
        fetch(`/api/user/${userId}`)
            .then((r) => {
                if (!r.ok) {
                    r.json().then(d => {throw new Error(d.error)})
                }
                return r.json()})
            .then((data) => {
                setProfileInfo(data['profile_info'])
                setMyProfile(data['my_profile'])
                setFavorited(data['favorite_status'])
                setLiked(data['liked'])
            })
            .catch((e) => { 
                console.log(e)
            })

    }, [userId])


    const handleMessageUser = () => {
        //Conversations - post
        fetch('/api/conversations',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userId: userId,
            })
        })
       .then(r => {
            if (!r.ok) {
                r.json().then(d => {throw new Error(d.error)})
            }
            return r.json()
        })
        .then((data) => {
            navigate("/message")
        })
        .catch((err) => {
            console.log(err)
        })

    }


    const handleJudgement = (judgement) => {
        //Matches - post
        fetch('/api/match',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userId: userId,
                judgement: judgement
            })
        })
        .then(r => {
            if (!r.ok) {
                throw new Error(r.statusText)
            }
            return r.json()
        })
        .then((data) => {
            // do something to disable button when it's pressed maybe?
            setLiked((liked) =>judgement)
        })
        .catch((e) => { 
            console.log(e)
        })

    }


    const handleAddFavorite = () => {
        //Favorites - post
        // probably going to want UserProfile to send if user has been favorited or not
        if (favorited === null || favorited === false) {
            fetch(`/api/favorites`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: userId,
                })
            }).then((r) =>{
                if (!r.ok) {
                    r.json().then(d => {throw new Error(d.error)})
                }
                return r.json()
            }).then((data) => {
                //set the favorited state when you create it
                setFavorited((favorited) =>!favorited)
            })
            .catch((e) => { 
                console.log(e)
            })
        }
        else {
            //Favorites - delete
            fetch(`/api/favorites`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: userId
                })
            }).then(r => {
                if (!r.ok) {
                    r.json().then(d => {throw new Error(d.error)})
                }
                setFavorited((favorited) =>!favorited)
            })
        }
    }

  
    console.log(profileInfo.ethnicity)
  return (
        <div>

    <Row className="justify-content-md-start pb-5">
        <Col md={{span: 3, offset: 1 }} >
            <img className='profile-pic' src={profileInfo.avatar_url} alt="Profile" />
        </Col>
        <Col md='auto' >
            <h4>{profileInfo.username}</h4>
            <h6>{profileInfo.age} / {profileInfo.gender} / {profileInfo.city} {profileInfo.state} ({profileInfo.distance} Mi) </h6>
            <h6> {profileInfo.liked === 'none' ? '' : profileInfo.liked ? 'LIKED!' : 'DISLIKED...'}</h6>

        </Col>
        <Col>
            { myProfile ? 
            <Stack gap={2} className="col-md-5 mx-auto">
            <Button variant="secondary" onClick={() => navigate(`/profile/${userId}/settings`)}>Settings</Button>
            <Button variant="secondary" onClick={() => navigate(`/profile/${userId}/upload-image/`)}>Add Photos</Button>
            <Button variant="secondary" onClick={() =>navigate(`/profile/${userId}/create-pet`) }>Add Pets</Button>
            </Stack>
            :
            <Stack gap={2} className="col-md-5 mx-auto">
                
                <Button variant="secondary" onClick={handleMessageUser}>Message</Button>
                <Button variant="outline-secondary" onClick={handleAddFavorite}>Favorite</Button>
                <DropdownButton  id="dropdown-basic-button" title="Matching">
                    <Dropdown.Item href="#/action-1" onClick={()=> handleJudgement(true)}>Like</Dropdown.Item>
                    <Dropdown.Item href="#/action-2" onClick={()=> handleJudgement(false)}>Pass</Dropdown.Item>
                </DropdownButton>
               
            </Stack>
            }
        </Col>
    </Row>
    <Row className="justify-content-start ml-md-5">
        <Col>
            <Tabs defaultActiveKey="about" id="uncontrolled-tab-example" className="px-1" justify >
                
                <Tab eventKey="about" title="About" className="px-1"  >
                    <About profileInfo={profileInfo}/>
                </Tab>
                <Tab eventKey="pets" title=" Pets  " className="custom-tab" >
                    <Pets myProfile={myProfile} />
                </Tab>
                <Tab eventKey="photos" title="Photos" className="custom-tab">
                    <Photos myProfile={myProfile}/>
                </Tab>
            </Tabs>
        </Col>
        <Col md={4}>
        <Card>
            <Card.Header>My Info</Card.Header>
            <Card.Body>
            
            <ListGroup variant="flush">
                <ListGroup.Item>Last Online: {profileInfo.last_online ===0 ? 'Today' :`${profileInfo.last_online} days ago`}</ListGroup.Item>
                <ListGroup.Item>Orientation: {profileInfo.orientation}</ListGroup.Item>
                <ListGroup.Item>Ethnicty: {profileInfo.ethnicity}</ListGroup.Item>
                <ListGroup.Item>Status: {profileInfo.status}</ListGroup.Item>
                <ListGroup.Item>Pets: {profileInfo.pet}</ListGroup.Item>
                <ListGroup.Item>Height: {`${Math.floor(profileInfo.height/12)}' ${profileInfo.height%12}" `}</ListGroup.Item>
                <ListGroup.Item>Diet: {profileInfo.diet}</ListGroup.Item>
                <ListGroup.Item>Religion:  {profileInfo.religion}</ListGroup.Item>
            </ListGroup>
            
            </Card.Body>
        </Card>
        </Col>
    </Row>
    </div>

  );
};

export default Profile;