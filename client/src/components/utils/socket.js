// utils/socket.js

import { setSocket } from '../actions/socket';
import io from 'socket.io-client';

export const setupSocket = (dispatch, username) => {
  const socket = io('http://localhost:5555', {
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