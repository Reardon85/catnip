import React, { useEffect, useState } from "react";
import { Routes, Route, useParams} from 'react-router-dom';
import './styles/app.css';
import { Tab, Tabs, ListGroup, Card, Button, Container, Row, Col, Navbar, Nav,  } from 'react-bootstrap';
import { Slide, Snackbar, Alert, Typography} from '@mui/material';

import 'bootstrap/dist/css/bootstrap.min.css'
import { socket } from './Socket';
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
import PetProfile from "./PetProfile";
import CreatePet from './CreatePet'
import ImageUpload from './ImageUpload'
import { useDispatch } from 'react-redux';
import { setupSocket } from './utils/socket';
import { useSelector } from 'react-redux';
import FavoriteBorderOutlinedIcon from '@mui/icons-material/FavoriteBorderOutlined';
import PriorityHighTwoToneIcon from '@mui/icons-material/PriorityHighTwoTone';
import ModeCommentTwoToneIcon from '@mui/icons-material/ModeCommentTwoTone';



function TransitionLeft(props) {
    return <Slide {...props} direction="left" />;
  }




  function App() {
    const { isLoading, error, isAuthenticated, getAccessTokenSilently } = useAuth0();
    const [newUser, setNewUser] = useState('empty');
    const [user, setUser] = useState(null);
    const [semaphore, setSemaphor] = useState(true);
    // const dispatch = useDispatch();
    // const socket = useSelector(state => state.socket.socket);
    const [open, setOpen] = useState(false);
    const [transition, setTransition] = useState(undefined);
    const [contents, setContents] = useState({message:"", avatar_url:'', username:'' });
    const [open2, setOpen2] = useState(false);
    const [transition2, setTransition2] = useState(undefined);
    const [contents2, setContents2] = useState({message:"", avatar_url:'', username:'' });
    const [o, setO] = useState(false);
    const [tran, setTran] = useState(undefined);
    const [c, setC] = useState({message:"", avatar_url:'', username:'' });
    const [newMsgs, setNewMsgs] = useState(0)
    const [newMatch, setNewMatch] = useState(0)
  
    const handleClose = () => {
      setOpen(false);
    };
    const handleClose2 = () => {
        setOpen2(false);
      };

      const handleC = () => {
        setO(false);
      };
  
    // useEffect(() => {
    //   setupSocket(dispatch, 'username');
    // }, [dispatch]);

    useEffect(()=> {

    



        if(semaphore && user){
            console.log('inside the semaphore')
            
            socket.on('msgNotify', data => {
                console.log(typeof(data))
                console.log("test brodfsfsfdsfsfsfsdfsfdss")
                setContents(()=> ({message:`New Message From `, avatar_url:data.avatar_url, username:data.username})) 
                setTransition(() => TransitionLeft);
                setOpen(true);
                setNewMsgs((newMsgs)=> newMsgs+1)
                console.log(newMsgs)
   
            });

            socket.on('favorites', data=> {
                console.log('inside Favorites listener1')
                setC(()=> ({message:`${data.username} Is Online! `, avatar_url:data.avatar_url})) 
                setTran(() => TransitionLeft);
                setO(true);
                
                
            })

            socket.on('matched', data=> {
                console.log('match %', data.match_percentage)
                console.log('test matched')
                setContents2(()=> ({message:`You Matched! ${data.match_percentage}%`, avatar_url:data.avatar_url})) 
                setTransition2(() => TransitionLeft);
                setOpen2(true);
                setNewMatch((newMatch)=> newMatch+1)
            })


            socket.emit('start', {userId:user.id})
            setSemaphor((semaphore)=> !semaphore)



        }

        return() => {
            console.log('inside the return socket off')
            socket.off('msgNotify',)
            socket.off('favorites')
            socket.off('matched')

        }

    },[user])

    console.log('checking on user', user)
    
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
            setUser(()=>data.user)
        } catch (e) {
            console.log(e.message);
        }
        };
  
    loginUser();
  }, [getAccessTokenSilently, isAuthenticated]);

  if (error) {
    return <div>Oops.. {error.message}</div>
  }





// if (true){
//     return (
//         <PhotoCarousel></PhotoCarousel>
//     )

// }

console.log('isLoading: ', isLoading)
console.log('isAuth: ', isAuthenticated )
console.log('newuser ', newUser)
console.log('user ', user)

if(isLoading){
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

if(!user){
    return (
        <div className="site">
            <Container fluid className="px-md-5">
                
            </Container>
        </div>
    )
  }



return (
<>
<div className="site">



   
    <Navigation user={user} newMatch={newMatch} setNewMatch={setNewMatch} newMsgs={newMsgs} setNewMsgs={setNewMsgs}/>
    <Container fluid className="px-md-5">
        
        <Routes>

            <Route path="/" exact element={<Home />} />
            <Route exact path='/profile/:userId' element={<Profile user={user}/>} />
            <Route exact path='/match' element={<Match/>} />
            <Route exact path="/messages/:userId" element={<MessageCenter  user={user}/>} />
            <Route path="/search" element={<Search/>} />
            <Route path='/profile/:userId/settings' element={<Settings user={user} setUser={setUser}/>} />
            <Route path='/profile/:userId/pet/:petId' element={<PetProfile/>} />
            <Route path='/profile/:userId/create-pet' element={<CreatePet />} />
            <Route path='/profile/:userId/upload-image/' element={<ImageUpload />} />
            <Route path='/profile/:userId/pet/:petId/upload-image/' element={<ImageUpload />} />
        </Routes>
        <Snackbar
                open={open2}
                onClose={handleClose2}
                TransitionComponent={transition2}
                message="I love snacks"
                key={transition2 ? transition2.name : ''}>
                        <Alert icon={<FavoriteBorderOutlinedIcon fontSize="inherit" />} onClose={handleClose} severity="error" sx={{ width: '100%' }}>
                            
                            <img className="user-convo-photo" src={contents2.avatar_url} alt="dumb"/>{contents2.message}{contents.match_percentage}
                            
                        </Alert>
            </Snackbar> 
            <Snackbar
                open={open}
                onClose={handleClose}
                TransitionComponent={transition}
                message="I love snacks"
                key={transition ? transition.name : ''}>
                        <Alert icon={<ModeCommentTwoToneIcon  />} onClose={handleClose} severity="info" sx={{ width: '100%' }}>
                        
                        <Typography  sx={{fontSize:'1em', fontWeight: 'bold', color:'#133850'  }} >
                        <img className="user-notify-photo" src={contents.avatar_url} alt="dumb"/>
                            {contents.message} 
                           
                            {contents.username}
                        </Typography>
                        </Alert>
            </Snackbar>  

  

    <Snackbar
                open={o}
                onClose={handleC}
                TransitionComponent={tran}
                key={tran ? tran.name : ''}>
                        <Alert icon={<PriorityHighTwoToneIcon />} severity="success" onClose={handleC}  sx={{ width: '100%' }}>
                        
                        <Typography  sx={{fontSize:'1em', fontWeight: 'bold', color:'#133850'  }} >
                        <img className="user-notify-photo" src={c.avatar_url} alt="dumb"/>
                            {c.message} 
                           
                            
                        </Typography>
                        </Alert>
            </Snackbar>  

    </Container>
</div>
</>
);
}


//     </div>
//   )
// }

export default App;


