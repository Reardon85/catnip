import { SET_SOCKET } from '../actions/socket';

const initialState = {
  socket: null
};

const socketReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_SOCKET:
      return {
        ...state,
        socket: action.socket
      };
    default:
      return state;
  }
};

export default socketReducer;