import React from 'react';
import './Sidebar.css';

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="user-info">
        
        <h3>Store Clerk</h3>
        <p>storeclerk@gmail.com</p>
      </div>
      <nav>
        <button className="active">Home</button>
        <button>Stock Summary</button>
        <button>Issue Item</button>
        <button>Manage Stock</button>
        <button>Adjust Stock</button>
        <button className="logout">Log Out</button>
        <p className="logo-label">ICT Authority</p>
      </nav>
    </aside>
  );
}
