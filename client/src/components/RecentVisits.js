import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";

const RecentVisits = () => {

  const [visitedList, setVisitedList] = useState([])


  useEffect(() => {
    fetch(`/api/visited`)

        .then((r) => {
            if (r.ok) {
                r.json().then((data) => {
                    setVisitedList(data)
                    console.log(data)
                })
            }
        })

}, [])
  

const visitArray = visitedList.map((visit) => (
  <div className={'conversation-div'}>
    <Link to={`/profile/${visit.user_id}`}   style={{ textDecoration: 'none', color: 'inherit' }}>
    <img src={visit.avatar_url} alt='profile' className='user-convo-photo' />
    {visit.username}
    </Link>
  </div>
))

  return (
    <div>
      <h5>Recently Visited:</h5>
      {visitArray}
    </div>

  );
};

export default RecentVisits;