import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link, useParams, useNavigate } from "react-router-dom";
import { Tab, Tabs, ListGroup, Card, Row, Col} from 'react-bootstrap';
import Photos from './Photos';
import About from './About';

const PetProfile = () => {

    const [petInfo, setPetInfo] = useState({})
    const {petId} = useParams
    const navigate = useNavigate()

    useEffect(() => {
        //Pet_Profiles - get
        fetch(`/api/pet/${petId}`)
        .then(res => {
            if(!res.ok){
                res.json().then(err => {throw new Error(err.message)})
            }
            res.json()
        })
        .then(data => {
            setPetInfo(data)
        })    

    }, [petId])


    const handleRemovePet = () => {
        //Pet_Profiles - delete
        fetch(`/api/petphotos/${petId}`, {
            method: 'DELETE',
        }).then(res => {
            if(!res.ok){
                res.json().then(err => {throw new Error(err.message)})
            }
            return res.json()
        }).then(data => {
            navigate('/')
        })
        .catch(err => {
            console.log(err)
        })
    } 
  
  
  return (
    <div>

    <Row className="justify-content-md-start pb-5">
        <Col md={{span: 3, offset: 1 }} >
            <img src={'https://the-tea.s3.us-east-2.amazonaws.com/profile1.jpg'} alt="Profile" />
        </Col>
        <Col md='auto' >
            <h2>{'name'}</h2>
            <h2>{'age'}</h2>
            <h2>{'distance'}</h2>
         </Col>
    </Row>
    <Row className="justify-content-start ml-md-5">
        <Col>
        <Tabs defaultActiveKey="about" id="uncontrolled-tab-example" className="px-1" justify >
            
            <Tab eventKey="about" title="About" className="px-1"  >
                <About />
            </Tab>
            <Tab eventKey="photos" title="Photos" className="custom-tab">
                <Photos />
            </Tab>
        </Tabs>
        </Col>
        <Col md={4}>
        <Card>
            <Card.Header>Card Title</Card.Header>
            <Card.Body>
            <Card.Title>Special title treatment</Card.Title>
            <ListGroup variant="flush">
            <ListGroup.Item>Last Online</ListGroup.Item>
            <ListGroup.Item>Orientation</ListGroup.Item>
            <ListGroup.Item>Ethnicty</ListGroup.Item>
            <ListGroup.Item>Status</ListGroup.Item>
            <ListGroup.Item>Pets</ListGroup.Item>
            <ListGroup.Item>Height</ListGroup.Item>
            <ListGroup.Item>Diet</ListGroup.Item>
            <ListGroup.Item>Religion</ListGroup.Item>
        </ListGroup>
            
            </Card.Body>
        </Card>
        </Col>
    </Row>
    </div>

  );
};

export default PetProfile;