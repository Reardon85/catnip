import React from 'react';
import './index.css'
import ReactDOM from 'react-dom';
import App from './components/App';
import { Auth0Provider } from "@auth0/auth0-react";
import { BrowserRouter as Router } from 'react-router-dom';

ReactDOM.render(
  <Auth0Provider
    domain="dev-yxel2dejc2kr1a0k.us.auth0.com"
    clientId='u14eAuErNPhorJHv5ctsBMztZJXNzqiK'
    authorizationParams={{
      
      audience: 'https://dev-yxel2dejc2kr1a0k.us.auth0.com/api/v2/',
      scope: "read:current_user update:current_user_metadata"
    }}>

  <React.StrictMode>
    <Router>
      <App />
    </Router>
  </React.StrictMode>
  </Auth0Provider>,
  document.getElementById('root')
);