import React from 'react';

import { Link } from 'react-router-dom';

const Message = ({ username, content, timestamp, avatar, userId }) => {
  return (
    <div className="comment">
      <div className="comment-header">
        <Link to={`/profile/${userId}`}>
        <img className="user-convo-photo" src={avatar} alt="Author's profile" />
        </Link>
        <h3 className="comment-author">{username}</h3>
      </div>
      <p className="comment-text">{content}</p>
      <p className="comment-timestamp">{new Date(timestamp).toLocaleString()}</p>
    </div>
  );
};

export default Message;