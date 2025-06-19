import React from 'react';
import './Sidebar.css';
import profile from '../assets/profile.png';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="profile">
         <img src={profile} alt="Profile" className="profile" />
        <h4>Store Clerk</h4>
        <p>storeclerk@gmail.com</p>
      </div>
      <ul className="menu">
        <li>🏠 Home</li>
        <li>📊 Stock Summary</li>
        <li>📦 Issue Item</li>
        <li>🛠️ Manage Stock</li>
        <li>⚙️ Adjust Stock</li>
        <li className="logout">🚪 Log Out</li>
        <li className="footer">🌐 ICT Authority</li>
      </ul>
    </div>
  );
};

export default Sidebar;
