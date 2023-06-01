import React, { useEffect, useState } from 'react';
import './styles/app.css';
import {Link, useParams } from "react-router-dom";
import { Tab, Tabs, ListGroup, Card, Row, Col} from 'react-bootstrap';



const Pets = () => {

    const [petList, setPetList] = useState([]);
    const {userId} = useParams();

    useEffect(() => {
        //User_Pets - get
        fetch(`/api/user/pets/${userId}`)
        .then(r => {
            if(!r.ok) {
                console.log(r)
            }
            return r.json()
        }).then(data => {
            setPetList(data)
        })
    }, [userId])
    
  
  
    return (
        <div>
            Show all Your pets
        </div>


  );
};

export default Pets;