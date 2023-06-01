import React, {useEffect, useState} from 'react';
import {Link } from "react-router-dom";
import AliceCarousel from 'react-alice-carousel';
import 'react-alice-carousel/lib/alice-carousel.css';
import {  Select, MenuItem, FormControl, InputLabel, Box, Button, Slider, Typography, Paper, Container, Card, CardContent, CardMedia, Grid } from '@mui/material';

const items = [
    <div className="item" data-value="1">1</div>,
    <div className="item" data-value="2">2</div>,
    <div className="item" data-value="3">3</div>,
    <div className="item" data-value="4">4</div>,
    <div className="item" data-value="5">5</div>,
];

const QuickMatch = () => {


  const [quickMatches, setQuickMatches] = useState([]);
  const [currentMatch, setCurrentMatch] = useState({})


  useEffect(()=> {
    //Quick_Matches - get
    fetch('/api/quick-match')
        .then((r) => {
            if(!r.ok){
                throw new Error(r.error)
            }
            return r.json()
        })
        .then((data) => {
            console.log(data)
            setCurrentMatch(()=>data[0])
            setQuickMatches(()=>data.slice(1))
            
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
            userId: currentMatch.id,
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
        setCurrentMatch(()=> quickMatches[0])
        setQuickMatches((quickMatches)=> quickMatches.slice(1))
    })
    .catch((e) => { 
        console.log(e)
    })
  }
  console.log(quickMatches)
  // So the plan is to map out the photos here
  // You will design it so the users other information will appear on the page
  // When they click to choose to like or dislie a user we will setQuickMatches((quickMatches) => quickMatches.pop())
  // hopefully that will work. 
  console.log("quickmatch")
  console.log(quickMatches)
  const items =  currentMatch?.photos ? currentMatch.photos.map((item) => {
    return (
        <div className="item" data-value={item.id}>
            <img src={item.image_url} alt='quick match'/>
        </div>
    )
  }) : []

  
  


    return (
        <Grid container justifyContent="center" alignItems="center" style={{ height: '100vh' }}>
          <Grid item xs={6}>
            <Card>
                <Box marginTop={5} marginLeft={13}  style={{ width: "80%"}}>
            <AliceCarousel
        animationType="fadeout" 
        animationDuration={800}
        disableButtonsControls
        infinite
        items={items}
        mouseTracking
    />
    </Box>
              <CardContent>
                <Typography variant="h5" component="div">
                  {currentMatch.username}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Age: {currentMatch.age}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Location: {currentMatch.distance}
                </Typography>
                <Button variant="contained" color="primary" onClick={()=> handleJudgement(true)}>
                  Like
                </Button>
                <Button variant="contained" color="secondary" onClick={()=> handleJudgement(false)}>
                  Pass
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>




  );
};

export default QuickMatch;