import React, {useEffect, useState} from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import MessageForm from './components/MessageForm';

const MessageCenter = () => {
	const [conversations, setConversations] = useState([])
	const [convoId, setConvoId] = useState(null)
  
	useEffect(() => {
  
		fetch('/api/conversations')
			.then((r) => r.json())
			.then((d)=> {
			  setConversations(d.list)
			  setConvoId(d['convo_id'])
			})
  
	}, [])
  
  
	
	
	const convoArray = conversations.map((convo) => (
	  <div className={convo.seen ? 'conversation-div' : 'conversation-div-unseen'} onClick={()=> setConvoId(convo.id)}>
		<img src={convo.avatar_url} alt='profile' className='user-convo-photo' />
		{convo.username}
	  </div>
	))
	
	return (
	  <div className="discussion-container">
		<div className="discussion-card">
		  {convoArray}
		</div>
		<div className="message-form-container">
		  <MessageForm convoId={convoId} />
		</div>
	  </div>
	);
};

export default MessageCenter;