import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const ActiveFavorites = () => {

     const [favOnline, setFavOnline] = useState([])


    useEffect(() => {
        // Favorites - get
        fetch(`/api/favorites`)

            .then((r) => {
                if (!r.ok) {
                    throw new Error(r.statusText)   
                }
                return r.json()
            })
            .then(data => {
                setFavOnline(data)
            })
            .catch((err)=> console.log(err))



    }, [])


    const favoriteArray = favOnline.map((favorite) => (
        <Link to={`/profile/${favorite.user_id}`}   style={{ textDecoration: 'none', color: 'inherit' }}>
        <img src={favorite.avatar_url} alt='profile pic' className='user-convo-photo'/> {favorite.username}
        </Link>

    ))

  
  
  return (
    <div>
      <h4>Curerntly Online Favorites</h4>
      {favoriteArray}
    </div>

  );
};

export default ActiveFavorites;