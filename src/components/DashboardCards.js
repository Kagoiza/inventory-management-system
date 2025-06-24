import React from 'react';
import './DashboardCards.css';

const DashboardCards = () => {
  return (
    <div className="cards">
      <div className="card green">Total Stock Items<br /><strong>50</strong></div>
      <div className="card green">Items Issued<br /><strong>35</strong></div>
      <div className="card green">Items Returned<br /><strong>20</strong></div>
    </div>
  );
};

export default DashboardCards;
