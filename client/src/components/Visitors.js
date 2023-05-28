import React, {useEffect, useState} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const Visitors = () => {
  
  const[visitorList, setVisitorList] = useState([])


  useEffect(() => {

    // Visitors - get
    fetch(`/api/visitors`)

        .then((r) => {
            if (r.ok) {
                r.json().then((data) => {
                    setVisitorList(data)
                    
                })
            }
        })

}, [])
  

const visitArray = visitorList.map((visit) => (
  <div className={'conversation-div'}>
    <Link to={`/profile/${visit.visitor_id}`}   style={{ textDecoration: 'none', color: 'inherit' }}>
    <img src={visit.avatar_url} alt='profile' className='user-convo-photo' />
    {visit.username}   [{visit.last_visit}]
    </Link>
    
  </div>
))
  
  return (
    <div>
      Show the last 20 people who visited you...
      {visitArray}
    </div>

  );
};

export default Visitors;