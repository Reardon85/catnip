import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import {   Box } from '@mui/material';


const About = ({profileInfo}) => {

  
  
  return (
    <div>
      <Box marginY={5}>
      <h3>Self-Summary:</h3>
      {profileInfo.bio}
      </Box>
      <Box marginTop={2}>
      <h3>Hobbies:</h3>
      {profileInfo.hobbies}
      </Box>
    </div>
    

  );
};

export default About;