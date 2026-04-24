import React from 'react';
import './Message.css';

const Message = ({ message }) => {
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString();
  };

  const isToday = (timestamp) => {
    const today = new Date();
    const messageDate = new Date(timestamp);
    return today.toDateString() === messageDate.toDateString();
  };

  return (
    <div className={`message ${message.sender}-message ${message.isError ? 'error' : ''}`}>
      <div className="message-avatar">
        {message.sender === 'user' ? '👤' : '🤖'}
      </div>
      
      <div className="message-content">
        <div className="message-text">
          {message.text}
        </div>
        
        {message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <p className="sources-label">Sources:</p>
            <ul className="sources-list">
              {message.sources.map((source, index) => (
                <li key={index} className="source-item">
                  📄 {source}
                </li>
              ))}
            </ul>
          </div>
        )}
        
        <div className="message-timestamp">
          {isToday(message.timestamp) 
            ? formatTime(message.timestamp)
            : `${formatDate(message.timestamp)} ${formatTime(message.timestamp)}`
          }
        </div>
      </div>
    </div>
  );
};

export default Message; 