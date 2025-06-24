import React from 'react';
import './RequestSummaryCard.css';

const RequestSummaryCard = ({ label, value, color }) => {
  return (
    <div className={`summary-card ${color}`}>
      <p className="card-label">{label}</p>
      <h3 className="card-value">{value}</h3>
    </div>
  );
};

export default RequestSummaryCard;
