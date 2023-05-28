import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const ActiveFavorites = () => {


  useEffect(() => {
    // Favorites - get
    fetch(`/api/favorites`)

        .then((r) => {
            if (r.ok) {
                r.json().then((data) => {
                    
                })
            }
        })

}, [])

  
  
  return (
    <div>
      Curerntly Online Favorites
    </div>

  );
};

export default ActiveFavorites;