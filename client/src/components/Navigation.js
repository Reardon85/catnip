import React, {useEffect, useState} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import { Navbar, Nav } from 'react-bootstrap';
import {Badge } from '@mui/material';
import io from 'socket.io-client';

const socket = io('http://localhost:5555');

const Navigation = ({user, newMsgs, setNewMsgs, newMatch, setNewMatch}) => {

  useEffect(()=> {


    

  },[])
    console.log(newMsgs)
  return (
    <Navbar bg="light"  expand="lg" >
    <Navbar.Brand href="/" className="px-3">CatNip</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to="/">Home</Nav.Link>
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to={`/profile/${user.id}`}>Profile</Nav.Link>
        <Badge badgeContent={newMatch} color="primary">
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to="/match">Match</Nav.Link>
        </Badge>
        <Badge badgeContent={newMsgs} color="primary">
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to={`/messages/${user.id}`}>Message</Nav.Link>
          </Badge>
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to="/search">Search</Nav.Link>
        
      </Nav>
    </Navbar.Collapse>
  </Navbar>

  );
};

export default Navigation;