import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import {  Select, MenuItem, FormControl, InputLabel, Box, Button, Slider, Typography, Paper, Badge } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useSelector } from 'react-redux';

const ActiveFavorites = () => {

    const socket = useSelector(state => state.socket.socket);

     
    const [favOnline, setFavOnline] = useState([])

    useEffect(() => {
        // Favorites - get

        socket.on('favorites', data=> {
            console.log('SECOND inside Favorites listener')
            setFavOnline((favOnline)=> [...favOnline, data])
        })
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

    const StyledBadge = styled(Badge)(({ theme }) => ({
        '& .MuiBadge-badge': {
            
            backgroundColor: '#44b700',
           
            color: '#44b700',
            boxShadow: `0 0 0 2px ${theme.palette.background.paper}`,
            '&::after': {
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                borderRadius: '50%',
                animation: 'ripple 1.2s infinite ease-in-out',
                border: '1px solid currentColor',
                content: '""',
          },
        },
        '@keyframes ripple': {
          '0%': {
            transform: 'scale(.8)',
            opacity: 1,
          },
          '100%': {
            transform: 'scale(2.4)',
            opacity: 0,
          },
        },
      }));


        const favoriteArray = favOnline.map((favorite) => (
            <Link to={`/profile/${favorite.user_id}`}   style={{ textDecoration: 'none', color: 'inherit' }}>
                <StyledBadge
                overlap="circular"
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                variant="dot"
                >
                    <img src={favorite.avatar_url} alt='profile pic' className='user-favorite-photo'/> 
                </StyledBadge>
            </Link>

    ))

  
  
  return (
    <div>
      <h5>Curerntly Online Favorites</h5>
      {favoriteArray}
    </div>

  );
};

export default ActiveFavorites;