import React from 'react';
import './RequestorSidebar.css';

const RequestorSidebar = () => {
  return (
    <div className="requestor-sidebar">
      <div className="sidebar-nav">
        <button>🏠 Home</button>
        <button>📝 Request Item</button>
        <button>📊 Request Summary</button>
      </div>

      <div className="sidebar-footer">
        <button className="logout" onClick={() => window.location.href = '/login'}>🚪 Logout</button>
        <div className="footer-text">ICT Authority</div>
      </div>
    </div>
  );
};

export default RequestorSidebar;
