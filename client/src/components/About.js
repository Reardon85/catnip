import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import {   Box } from '@mui/material';


const About = ({bio, hobbies}) => {

  
  
  return (
    <div>
      <Box marginY={5}>
        <h3>Self-Summary:</h3>
        {bio}
      </Box>
      <Box marginTop={2}>
        {bio ? (
          <>
            <h3>Hobbies:</h3>
            {hobbies}
          </>
        ) : " "}
      </Box>
    </div>
  )};

export default About;