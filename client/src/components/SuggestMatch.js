import React, {useState, useEffect} from 'react';
import {Link } from "react-router-dom";
import AliceCarousel from 'react-alice-carousel';
import 'react-alice-carousel/lib/alice-carousel.css';

const responsive = {
    0: { items: 1 },
    150: { items: 2 },
    300: { items: 3 },
};


const images = ['https://the-tea.s3.us-east-2.amazonaws.com/image1.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image3.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image11.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image12.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image2.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image4.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image5.jpg',]
const items = [
    <div className="item" data-value="1"><img src={images[0]} alt='none'/></div>,
    <div className="item" data-value="2"><img src={images[1]} alt='none'/></div>,
    <div className="item" data-value="3"><img src={images[2]} alt='none'/></div>,
    <div className="item" data-value="4"><img src={images[3]} alt='none'/></div>,
    <div className="item" data-value="5"><img src={images[4]} alt='none'/></div>,
    
];

const SuggestMatch = () => {

  const [suggestMatches, setSuggestMatches] = useState([]);


  useEffect(()=> {
    //Sugested_Matches - get
    fetch('/api/suggested-matches')
        .then((r) => {
            if(!r.ok){
                throw new Error(r.Error)
            }
            return r.json()
        })
        .then((data) => {
            
            setSuggestMatches(data)
        })
        .catch((err) => { 
            
        })

  },[])

  const items = suggestMatches.map((item) => {
    return (
      
        <div className="item" data-value={item.id}>
          <Link to={`/profile/${item.id}`} >
            <img src={item.avatar_url} alt='potential match'/>
            <p>{item.username}</p>
          </Link>
        </div>
        
    )
  })

  
  
  return (
    <div>
      We Will Suggest like 5 matches here

      <AliceCarousel
        mouseTracking
        disableDotsControls
        items={items}
        responsive={responsive}
        controlsStrategy="alternate"
    />
    </div>

  );
};

export default SuggestMatch;