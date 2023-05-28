import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const CreatePet = () => {


  const handleAddPet = () => {
    // User_Pets - post
      fetch(`/api/user/pets/1`, {
        method: 'POST',
      })
  }

  
  
  return (
    <div>
      Create a Pet Obj
    </div>

  );
};

export default CreatePet;