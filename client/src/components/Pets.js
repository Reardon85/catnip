import React, { useEffect, useState } from 'react';
import './styles/app.css';
import {Link, useParams, useNavigate } from "react-router-dom";
import { Tab, Tabs, ListGroup, Row, Col} from 'react-bootstrap';
import { Card, CardContent, Select, MenuItem, FormControl, InputLabel, Box, Button, Slider, Typography, Paper, Grid, CardMedia } from '@mui/material';



const Pets = () => {

    const [petList, setPetList] = useState([]);
    const {userId} = useParams();
    const navigate = useNavigate()

    useEffect(() => {
        //User_Pets - get
        fetch(`/api/user/pets/${userId}`)
        .then(r => {
            if(!r.ok) {
                console.log(r)
            }
            return r.json()
        }).then(data => {
            setPetList(data)
        })
    }, [])

    

//    const petArray = petList?.map((pet) => (
//         <Grid item xs={12} sm={6} md={4} key={pet.id}>
//             <Card style={{ width: "80%", margin: "0 auto", maxHeight: "20vh" }} onClick={() => navigate(`/profile/${userId}/pet/${pet.id}`)}>
//             <img src={pet.avatar_url} alt='dumb' className='profile-pic'/>
//             <CardContent>
//                 <Typography gutterBottom variant="h5" component="div">
//                 {pet.name}
//                 </Typography>
//                 <Typography gutterBottom variant="h6" component="div">
//                 {pet.animal}
//                 </Typography>
//                 <Typography gutterBottom variant="h7" component="div">
                
//                 </Typography>
//             </CardContent>
//             </Card>
//         </Grid>
//         ))

    // const petArray =  => (
    //     <Card sx={{ maxWidth: 345 }}>
    //         <img src={result.avatar_url} alt='avatar' className='profile-pic'/>
    //     {/* <CardMedia
    //         sx={{ height: 'auto' }}
    //         image={result.avatar_url}
    //         title="avatar"
    //     /> */}
    //     <CardContent>
    //     <Typography gutterBottom variant="h5" component="div">
    //     {result.name}
    //     </Typography>
    //     {/* <Typography variant="body2" color="text.secondary">
    //     Lizards are a widespread group of squamate reptiles, with over 6,000
    //     species, ranging across all continents except Antarctica
    //     </Typography> */}
        // </CardContent>
        // </Card>

    // ))
        console.log('pet', petList)

    
    
  
  
    return (
        <Grid marginTop={6} container spacing={3}>
        {/* { petArray} */}
    </Grid>


  );
};

export default Pets;