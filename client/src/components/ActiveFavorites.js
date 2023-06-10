import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import { socket } from './Socket';
import { styled } from '@mui/material/styles';
import { useSelector } from 'react-redux';
import { CssBaseline, List, ListItemText, Avatar, ListItemAvatar, ListItem, Badge} from "@mui/material";

const ActiveFavorites = () => {

    // const socket = useSelector(state => state.socket.socket);

     
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
        <ListItem button component={Link} to={`/profile/${favorite.user_id}`} key={favorite.user_id}>
          <ListItemAvatar>
            <StyledBadge overlap="circular" anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }} variant="dot">
              <Avatar src={favorite.avatar_url} />
            </StyledBadge>
          </ListItemAvatar>
          <ListItemText primary={favorite.username} />
        </ListItem>
      ))
    
      return (
        <List>
          <ListItem>
            <ListItemText primary="Currently Online Favorites" />
          </ListItem>
          {favoriteArray}
        </List>
      );
    };
export default ActiveFavorites;