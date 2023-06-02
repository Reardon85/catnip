import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import { CssBaseline, List, ListItemText, Avatar, ListItemAvatar, ListItem} from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";

const RecentVisits = () => {

  const [visitedList, setVisitedList] = useState([])


  useEffect(() => {
    fetch(`/api/visited`)

        .then((r) => {
            if (r.ok) {
                r.json().then((data) => {
                    setVisitedList(data)
                    console.log(data)
                })
            }
        })

}, [])
  

const visitArray = visitedList.map((visit) => (
  <ListItem button component={Link} to={`/profile/${visit.user_id}`} key={visit.user_id}>
    <ListItemAvatar>
      <Avatar src={visit.avatar_url} />
    </ListItemAvatar>
    <ListItemText primary={visit.username} />
  </ListItem>
))

return (
  <List>
    <ListItem>
      <ListItemText primary="Recently Visited:" />
    </ListItem>
    {visitArray}
  </List>
);
};
export default RecentVisits;