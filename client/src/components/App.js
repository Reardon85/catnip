import React, { useEffect, useState } from "react";
import { Routes, Route, useParams} from 'react-router-dom';
import './styles/app.css';
import { Tab, Tabs, ListGroup, Card, Button, Container, Row, Col, Navbar, Nav } from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.min.css'

import LoginButton from "./LoginButton";
import LogoutButton from "./LogoutButton";
import { User, useAuth0 } from "@auth0/auth0-react";

import Navigation from "./Navigation";
import Home from "./Home";
import Profile from "./Profile";
import Match from "./Match";
import MessageCenter from "./MessageCenter";
import Search from "./Search";
import NewAccount from "./NewAccount";
import Settings from "./Settings";
import Pets from "./Pets"
import CreatePet from './CreatePet'
import ImageUpload from './ImageUpload'






function App() {
  // Code goes here!
  const { isLoading, error, isAuthenticated, getAccessTokenSilently} = useAuth0()
  const [newUser, setNewUser] = useState('empty')
  const [user, setUser] = useState(null)

 

    useEffect(() => {
        const loginUser = async () => {

 
        
        try {
            const accessToken = await getAccessTokenSilently();
            const response = await fetch('/api/login', {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
            });
            /// handle response here Important if it's a new user.
            const data = await response.json()  
            setNewUser(data.newUser)
            setUser(data.user)
        } catch (e) {
            console.log(e.message);
        }
        };
  
    loginUser();
  }, [getAccessTokenSilently, isAuthenticated]);

  if (error) {
    return <div>Oops.. {error.message}</div>
  }
  console.log(newUser)
  console.log(user)




// if (true){
//     return (
//         <PhotoCarousel></PhotoCarousel>
//     )

// }




if(isLoading || !user){
    return (
        <div className="site">
            <Container fluid className="px-md-5">
                
            </Container>
        </div>
    )
  }

if (!isAuthenticated){
    return (
        <div className="site">
            <Container fluid className="px-md-5">
                <LoginButton></LoginButton>
            </Container>
        </div>
    )
}


if (newUser===true){
    return (
        <div className="site">
            <Container fluid className="px-md-5">
                <NewAccount setNewUser={setNewUser} setUser={setUser}/>
            </Container>
        </div>
    )    
}



return (
<>
<div className="site">



    <LogoutButton/>
    <Navigation user={user} />
    <Container fluid className="px-md-5">
        <Routes>
            <Route path="/" exact element={<Home/>} />
            <Route path='/profile/:userId' element={<Profile/>} />
            <Route path='/match' element={<Match/>} />
            <Route path="/message" element={<MessageCenter/>} />
            <Route path="/search" element={<Search/>} />
            <Route path='/profile/:userId/settings' element={<Settings user={user} setUser={setUser}/>} />
            <Route path='/profile/:userId/pet/:petId' element={<Pets/>} />
            <Route path='/profile/:userId/create-pet' element={<CreatePet />} />
            <Route path='/profile/:userId/upload-image/' element={<ImageUpload />} />
            <Route path='/profile/:userId/pet/:petId/upload-image/' element={<ImageUpload />} />
        </Routes>


    </Container>
</div>
</>
);
}


//     </div>
//   )
// }

export default App;
