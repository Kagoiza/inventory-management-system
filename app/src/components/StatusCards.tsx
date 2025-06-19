import React from 'react';

const StatusCards: React.FC = () => {
  return (
    <div className="status-cards">
      <div className="card green">
        <h3>Completed Audits</h3>
        <p>15</p>
      </div>
      <div className="card gray">
        <h3>Pending Audits</h3>
        <p>5</p>
      </div>
      <div className="card gray">
        <h3>Issues Found</h3>
        <p>0</p>
      </div>
    </div>
  );
};

export default StatusCards;
