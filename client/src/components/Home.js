import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import ActiveFavorites from './ActiveFavorites';
import SuggestMatch from './SuggestMatch'
import RecentVisits from './RecentVisits'
import {  Select, MenuItem, FormControl, InputLabel, Box, Button, Slider, Typography, Paper, Badge, Grid } from '@mui/material';

const Home = () => {

  
  
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <SuggestMatch />
      </Grid>
      <Grid item xs={1} />
      <Grid  item xs={5}>
        <RecentVisits />
      </Grid>
      <Grid item xs={6}>
        <ActiveFavorites />
      </Grid>
      <Grid item xs={12} style={{ height: '60px' }} /> {/* Padding/Margin at the bottom */}
    </Grid>
  );
};

export default Home;