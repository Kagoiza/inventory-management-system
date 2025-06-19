import React from 'react';
import './Header.css';
import logo from '../assets/logo.png';
const Header = () => {
  return (
    <div className="header">
       <img src={logo} alt="Logo" className="logo" />
      <h2>WELCOME!</h2>

      <div className="buttons">
        <button>Issue Item</button>
        <button>Manage Stock</button>
        <button>Adjust Stock</button>
      </div>
    </div>
  );
};

export default Header;
