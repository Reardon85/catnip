import React from 'react';
import './styles/app.css';
import {useParams } from "react-router-dom";

import { Tab, Tabs, Row, Col } from 'react-bootstrap';
import SettingsBasic from './SettingsBasic';
import SettingsMyInfo from './SettingsMyInfo';
import SettingsLookingFor from './SettingsLookingFor';
import {Snackbar, Button } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

const Settings = ({user, setUser}) => {

    const {userId} = useParams()
    const [open, setOpen] = React.useState(false);
    const [state, setState] = React.useState({
        open: false,
        vertical: 'top',
        horizontal: 'center',
      });
      const { vertical, horizontal, openn } = state;

    const handleClick = () => {
      setOpen(true);
    };
  
    const handleClose = (event, reason) => {
      if (reason === 'clickaway') {
        return;
      }
  
      setOpen(false);
    };
  
    const action = (
      <React.Fragment>

        <IconButton
          size="small"
          aria-label="close"
          color="inherit"
          onClick={handleClose}
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      </React.Fragment>
    );

    const handleUpdateAccount = (formData) => {
    // MAKE THIS A A PATCH
    //User_Profiles - post
        fetch(`/api/user/${userId}`, {
            method: 'PATCH',
            body: formData
        })
        .then(r => {
            if(!r.ok){
                throw new Error(r.statusText)
            }
            
            return r.json()
            
        })
        .then(data => setUser(()=> data))
        .catch((err) => console.log('error occured:', err))
        setOpen(true);
    }

    const handleDeleteAccount = () => {
        //User_Profiles - delete
        fetch(`/api/user/${userId}`, {
            method: 'DELETE',
        })
    }
  
  
    return (
        <div>
            <Row className='justify-content-start ml-md-5'>
                <h2>Settings</h2>
            </Row>
            <Row classname='justify-content-start ml-md-5'>
                <Col>
                    <Tabs defaultActiveKey='basic' id='settings' className='px-1' justify>
                        <Tab eventKey='basic' title='Basic'> 
                            <SettingsBasic user={user} onUpdateAccount={handleUpdateAccount} onDeleteAccount={handleDeleteAccount} />
                        </Tab>
                        <Tab eventKey='my-info' title="My Info">
                            <SettingsMyInfo user={user} onUpdateAccount={handleUpdateAccount}/>
                        </Tab>
                        <Tab eventKey='looking-for' title='Looking For'>
                            <SettingsLookingFor user={user}  onUpdateAccount={handleUpdateAccount} />
                        </Tab>

                    </Tabs>
                </Col>
            </Row>
            
<Snackbar
  open={open}
  autoHideDuration={6000}
  anchorOrigin={{ vertical, horizontal }}
  onClose={handleClose}
  message="Account Has Been Updated!"
  action={action}
/>
        </div>

    );
};

export default Settings;