import React from 'react';
import './SummaryCard.css';

export default function SummaryCard({ label, value, type }) {
  return (
    <div className={`summary-card ${type}`}>
      {label}<br /><span>{value}</span>
    </div>
  );
}
