import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const ImageUpload = () => {




  const handleUserImage = () => {
    //User_Photos - post
    fetch(`/api/user/photos/1`, {
      method: 'POST',
 
    })
  }

  
  
  return (
    <div>
      Upload an image...
    </div>

  );
};

export default ImageUpload;