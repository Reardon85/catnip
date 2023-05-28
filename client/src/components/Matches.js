import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const Matches = () => {

  const [matchList, setMatchList] = useState([])


  useEffect(()=> {
    //Matches - get
    fetch('/api/match')
        .then((r) => {
            if(!r.ok){
                r.json().then((data) => {throw new Error(data.error)})
            }
            return r.json()
        })
        .then((data) => {
            setMatchList(data)
        })
        .catch((err) => { 
            console.log(err)
        })

  },[])


  const matchArray = matchList.map((match) => (
    <div className={'conversation-div'}>
      <Link to={`/profile/${match.id}`}   style={{ textDecoration: 'none', color: 'inherit' }}>
      <img src={match.avatar_url} alt='profile' className='user-convo-photo' />
      {match.username}
      </Link>
      
    </div>
  ))

  
  
  return (
    <div>
      List of Matches
      {matchArray}
    </div>

  );
};

export default Matches;