import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import ActiveFavorites from './ActiveFavorites';
import SuggestMatch from './SuggestMatch'
import RecentVisits from './RecentVisits'

const Home = () => {

  
  
  return (
    <div>
      <SuggestMatch />
      <RecentVisits />
      <ActiveFavorites />

    </div>

  );
};

export default Home;