import React, { useState, useEffect } from 'react';
import Messages from './Messages';



const MessageForm = ({ convoId }) => {
  const [message, setMessage] = useState('');
  const [messageList, setMessageList] = useState([])

  console.log(convoId)

  useEffect(() => {


    

    // socket.on('receive_message', data => {
    //   console.log("the socket worked")
    //   console.log(data)
    //   setMessageList(prevMessages =>  prevMessages.concat(data));
    // });

   
    // socket.emit('join', convoId);

    fetch(`api/messages/${convoId}`)
      .then((r) => r.json())
      .then((d) => setMessageList(d))

    // return () => socket.off("message");
  }, [convoId])
  

  const comment_array = messageList.map((c) => {
    return <Messages key={c.id} username={c.username} avatar={c.avatar_url} timestamp={c.created_at} content={c.text} userId={c.user_id} />
  })

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you would handle the comment submission, for instance, by calling an API endpoint.
    // socket.emit('send_message', { convoId:'uNhMcQatcz11xS7DAAAF', message }); 
    
    
    const message_info = {
      convoId: convoId,
      text: message,
    }

    fetch(`api/messages/${convoId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(message_info)
    }).then((r) => r.json())
      .then((d) => setMessageList((messageList) => messageList.concat(d)))


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