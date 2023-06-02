// utils/socket.js

import { setSocket } from '../actions/socket';
import io from 'socket.io-client';

export const setupSocket = (dispatch, username) => {
  const socket = io('https://catnip-7vlf.onrender.com', {
    query: { username }
  });

  // You can setup all your socket event listeners here

  socket.on('connect', () => {
    console.log('Connected to server');
    dispatch(setSocket(socket));
  });

  // ...

  return socket;
};