import React, { useState, useEffect } from 'react';
import Messages from './Messages';
import { useParams } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { socket } from './Socket';





const MessageForm = ({user, convoId, messageDict, setMessageDict }) => {
    const [message, setMessage] = useState('');
    const [messageList, setMessageList] = useState([])

    const [Nmessage, setNMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const {userId} = useParams()
    // const socket = useSelector(state => state.socket.socket);
    

 

    useEffect(() => {
        console.log('starting convoID', convoId)
        socket.emit('join', {  convoId, userId });

        socket.on('user_connected', data => {
            console.log('connected', data.Message)
            setMessages(prevMessages => [...prevMessages, data.message]);
        });

        socket.on('message', data => {
        console.log("test bro", data.message)
        setMessageDict((messageDict) => ({
            ...messageDict,
            [data.convoId]: [...(messageDict[data.convoId] || []), data],
        }));
        
        setMessages(prevMessages => [...prevMessages, data.message]);
        });

        return () => {
            console.log('cleanup convo id', convoId)
            socket.off('user_connected');
            socket.off('message');
        }
    }, [convoId])
   

    const comment_array = convoId ? 
        Object.values(messageDict[convoId]).map((c) => {
        return <Messages key={c.id} username={c.username} avatar={c.avatar_url} timestamp={c.created_at} content={c.text} userId={c.user_id} />
        }) 
        : " "


  const handleSubmit = (event) => {
    event.preventDefault();

    
 
    socket.emit('message', { convoId, message, userId });
    
    const message_info = {
      convoId: convoId,
      text: message,
    }

    // fetch(`api/messages/${convoId}`, {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json"
    //   },
    //   body: JSON.stringify(message_info)
    // }).then((r) => r.json())
    //   .then((d) => setMessageList((messageList) => messageList.concat(d)))


    setMessage('');
  }





  return (
    <>
      {comment_array}
      <form className="comment-form" onSubmit={handleSubmit}>
        <textarea
          className="comment-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Write your comment..."
        />
        <button className="com-btn" type="submit">Submit</button>
      </form>
    </>
  );
};

export default MessageForm;