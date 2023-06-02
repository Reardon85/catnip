// store/index.js

import { createStore, combineReducers } from 'redux';
import socketReducer from '../reducers/socket';

const rootReducer = combineReducers({
  socket: socketReducer,
  // other reducers...
});

const store = createStore(
  rootReducer,
  // other middleware...
);

export default store;