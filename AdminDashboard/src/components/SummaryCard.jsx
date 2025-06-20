import React from 'react';

const SummaryCard = ({ title, value, color }) => (
  <div className={`p-4 rounded-xl shadow text-white ${color}`}>
    <h3 className="text-sm">{title}</h3>
    <p className="text-2xl font-bold">{value}</p>
  </div>
);

export default SummaryCard;
