import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import { Navbar, Nav } from 'react-bootstrap';

const Navigation = ({user}) => {

  
  
  return (
    <Navbar bg="light"  expand="lg" >
    <Navbar.Brand href="/" className="px-3">CatNip</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to="/">Home</Nav.Link>
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to={`/profile/${user.id}`}>Profile</Nav.Link>
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to="/match">Match</Nav.Link>
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to="/message">Message</Nav.Link>
        <Nav.Link as={Link} className="nav-link fs-4 px-3" to="/search">Search</Nav.Link>
      </Nav>
    </Navbar.Collapse>
  </Navbar>

  );
};

export default Navigation;