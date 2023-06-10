import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link, useParams, useNavigate } from "react-router-dom";
import { Tab, Tabs, ListGroup, Card, Row, Col} from 'react-bootstrap';
import Photos from './Photos';
import About from './About';

const PetProfile = () => {

    const [petInfo, setPetInfo] = useState(null)
    const {petId} = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        //User_Profiles - get
        fetch(`/api/pet/${petId}`)
            .then((r) => {
                if (!r.ok) {
                    r.json().then(d => {throw new Error(d.error)})
                }
                return r.json()})
            .then((data) => {
               setPetInfo(data)
            })
            .catch((e) => { 
                console.log(e)
            })

    }, [])


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
        console.log(petInfo)

        if(!petInfo){
            return (
                <div>
                    "loading"
                </div>
            )
        }
  
  
    return (
 
        <div>
          <Row className="justify-content-md-start pb-5">
            <Col md={{span: 3, offset: 1 }} >
              <img src={petInfo.avatar_url} alt="Profile" className='profile-pic'/>
            </Col>
            <Col md='auto' >
              <h2>{petInfo.name}</h2>
              <h2>{petInfo.animal}</h2>
              <h2>{petInfo.size}</h2>
            </Col>
          </Row>
          <Row className="justify-content-start ml-md-5">
            <Col>
              <Tabs defaultActiveKey="about" id="uncontrolled-tab-example" className="px-1" justify >
                <Tab eventKey="about" title="About" className="px-1"  >
                  <About bio={petInfo.description} hobbies={false} />
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
   

  )
  

};

export default PetProfile;