import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Profile from "./Profile";
import LoginButton from "./LoginButton";
import LogoutButton from "./LogoutButton";
import { useAuth0 } from "@auth0/auth0-react";

function App() {
  // Code goes here!
  const { isLoading, error} = useAuth0()

  if (error) {
    return <div>Oops... {error.message}</div>
  }

  if(isLoading){
    return <div>Loading...</div>
  }
  

  return(
    <div>
    <LoginButton/>
    <LogoutButton/>
    <Profile/>


    </div>
  )
}

export default App;
