import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import SearchResults from './SearchResults.js';

const Search = () => {

  
  
  return (
    <div>
      This will let you do complex searches 
      <SearchResults />
    </div>

  );
};

export default Search;