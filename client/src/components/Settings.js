import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const Settings = () => {

  

  const handleUpdateAccount = () => {
    //User_Profiles - post
    fetch('/api/user/1', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: {}
    })
  }

  const handleDeleteAccount = () => {
    //User_Profiles - delete
    fetch('/api/user/1', {
      method: 'DELETE',
    })
  
  
  }
  
  
  return (
    <div>
      You will Edit your Settings here
    </div>

  );
};

export default Settings;