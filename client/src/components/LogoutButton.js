import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { socket } from './Socket';

const LogoutButton = ({setUser}) => {
    const { logout } = useAuth0();

    const onLogOut = () =>{


        fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
        })
        .then(r => {

            if(!r.ok){
                throw new Error(r.statusText) 
            }
            setUser(null)
            socket.disconnect()
            logout({ logoutParams: { returnTo: window.location.origin } })
        })
        .catch((err)=> console.log(err))



        

    }

    return (
        <button onClick={onLogOut}>
            Log Out
        </button>
    );
};

export default LogoutButton;