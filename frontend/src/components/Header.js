import React from 'react';
import './Header.css';

const Header = ({ isConnected }) => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <h1 className="logo">Internal Docs Q&A</h1>
        </div>
        
        <div className="header-right">
          <div className="status-container">
            <div className="connection-status">
              <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></span>
              <span className="status-text">
                {isConnected ? 'Backend Connected' : 'Backend Disconnected'}
              </span>
            </div>
          </div>
          
          <nav className="header-nav">
            <button className="nav-button" onClick={() => window.open('/health', '_blank')}>
              Health Check
            </button>
            <button className="nav-button" onClick={() => window.open('https://github.com', '_blank')}>
              Documentation
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 