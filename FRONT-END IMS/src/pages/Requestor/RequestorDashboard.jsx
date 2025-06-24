import React from 'react';
import './RequestorDashboard.css';
import RequestorSidebar from './RequestorSidebar';
import RequestSummaryCard from './RequestSummaryCard';
import RequestTable from './RequestTable';

const RequestorDashboard = () => {
  return (
    <div className="requestor-container">
      <RequestorSidebar />
      <div className="requestor-main">
        <h2 className="greeting">Hello Sarah!!</h2>

        <div className="dashboard-top">
          <button className="action-button">📥 Request Item</button>
          <input type="text" className="search-input" placeholder="Search for items..." />
        </div>

        <div className="summary-grid">
          <RequestSummaryCard label="Total Items Requested" value="5" color="green" />
          <RequestSummaryCard label="Approved" value="3" />
          <RequestSummaryCard label="Pending" value="1" />
        </div>

        <RequestTable />
      </div>
    </div>
  );
};

export default RequestorDashboard;
