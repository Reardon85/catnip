import React from 'react';
import './styles/app.css';
import {useNavigate } from "react-router-dom";
import {  Select, MenuItem, FormControl, InputLabel, Box, Button, Slider, Typography, Paper, Container, Card, CardContent, CardMedia, Grid } from '@mui/material';
import SearchCard from './SearchCard.js'


const SearchResults = ({searchResults}) => {

    const navigate = useNavigate()

// <SearchCard/>

    const searchArray = searchResults.map((result) => (
        <Card sx={{ maxWidth: 345 }}>
            <img src={result.avatar_url} alt='avatar' className='profile-pic'/>
        {/* <CardMedia
            sx={{ height: 'auto' }}
            image={result.avatar_url}
            title="avatar"
        /> */}
        <CardContent>
        <Typography gutterBottom variant="h5" component="div">
        {result.username}
        </Typography>
        {/* <Typography variant="body2" color="text.secondary">
        Lizards are a widespread group of squamate reptiles, with over 6,000
        species, ranging across all continents except Antarctica
        </Typography> */}
        </CardContent>
        </Card>

    ))


    return (

        <Grid container spacing={3}>
        {searchResults.map(user => (
        <Grid item xs={12} sm={6} md={4} key={user.id}>
            <Card style={{ width: "80%", margin: "0 auto" }} onClick={() => navigate(`/profile/${user.id}`)}>
            <CardMedia
                style={{
                    height: 0,
                    paddingTop: '100%', // 16:9 aspect ratio
                    backgroundSize: 'cover',
                    backgroundImage: `url(${user.avatar_url})`,
                    backgroundPosition: 'top',
                }}
            />
            <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                {user.username}
                </Typography>
                <Typography gutterBottom variant="h6" component="div">
                {user.match_percentage}%
                </Typography>
                <Typography gutterBottom variant="h7" component="div">
                {user.age}/{user.gender}/{user.orientation} {`(${user.distance} miles)`}
                </Typography>
            </CardContent>
            </Card>
        </Grid>
        ))}
    </Grid>

    );
};

export default SearchResults;