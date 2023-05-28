import React, {useEffect, useState} from 'react';
import {Link } from "react-router-dom";
import AliceCarousel from 'react-alice-carousel';
import 'react-alice-carousel/lib/alice-carousel.css';

const items = [
    <div className="item" data-value="1">1</div>,
    <div className="item" data-value="2">2</div>,
    <div className="item" data-value="3">3</div>,
    <div className="item" data-value="4">4</div>,
    <div className="item" data-value="5">5</div>,
];

const QuickMatch = () => {


  const [quickMatches, setQuickMatches] = useState([]);


  useEffect(()=> {
    //Quick_Matches - get
    fetch('/api/suggested-matches')
        .then((r) => {
            if(!r.ok){
                r.json().then((data) => {throw new Error(data.error)})
            }
            return r.json()
        })
        .then((data) => {
            setQuickMatches(data)
        })
        .catch((err) => { 
            console.log(err)
        })

  },[])

  const handleJudgement = (judgement) => {
    //Matches - post
    fetch('/api/match',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            userId: quickMatches[0].user_id,
            judgement: judgement
        })
    })
    .then(r => {
        if (!r.ok) {
            r.json().then(d => {throw new Error(d.error)})
        }
        return r.json()
    })
    .then((data) => {
        // do something to disable button when it's pressed maybe?
        
    })
    .catch((e) => { 
        console.log(e)
    })
  }

  // So the plan is to map out the photos here
  // You will design it so the users other information will appear on the page
  // When they click to choose to like or dislie a user we will setQuickMatches((quickMatches) => quickMatches.pop())
  // hopefully that will work. 
  const items = quickMatches.photos.map((item) => {
    return (
        <div className="item" data-value={item.id}>
            <img src={item.avatar_url} alt='quick match'/>
        </div>
    )
  })

  
  
  return (
    <div>
      Place where you do quick matches
      <AliceCarousel
        animationType="fadeout" 
        animationDuration={800}
        disableButtonsControls
        infinite
        items={items}
        mouseTracking
    />
      
    </div>

  );
};

export default QuickMatch;