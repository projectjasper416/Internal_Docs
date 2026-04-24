import React, { useState, useEffect } from 'react';
import './App.css';
import Chatbot from './components/Chatbot';
import Header from './components/Header';

function App() {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Check if backend is connected
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      const response = await fetch('/health');
      if (response.ok) {
        setIsConnected(true);
      }
    } catch (error) {
      console.log('Backend not connected:', error);
      setIsConnected(false);
    }
  };

  return (
    <div className="App">
      <Header isConnected={isConnected} />
      <main className="main-content">
        <div className="container">
          <div className="welcome-section">
            <h1>Internal Docs Q&A Agent</h1>
            <p className="subtitle">
              Ask questions about your company's internal documentation and get instant answers.
            </p>
            {!isConnected && (
              <div className="connection-warning">
                <p>⚠️ Backend not connected. Please ensure the Flask server is running on port 5000.</p>
              </div>
            )}
          </div>
          <Chatbot isConnected={isConnected} />
        </div>
      </main>
    </div>
  );
}

export default App;
