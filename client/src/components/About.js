import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const About = ({profileInfo}) => {

  
  
  return (
    <div>
      <h3>Self-Summary:</h3>
      {profileInfo.bio}
    </div>

  );
};

export default About;