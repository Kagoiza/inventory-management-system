import React from 'react';
import Sidebar from './Sidebar';
import SummaryCard from './SummaryCard';
import StockTable from './StockTable';
import './StoreClerkDashboard.css';

export default function StoreClerkDashboard() {
  const stockItems = [
    { id: 1, type: 'Laptop', status: 'Approve', expiration: 'May 15, 2025' },
    // ... other items
    { id: 2, type: 'Router', status: 'Approve', expiration: 'Mar 22, 2025' }
  ];

  return (
    <div className="dashboard">
      <Sidebar />
      <main className="main-content">
        <h1>STORE CLERK DASHBOARD</h1>

        <div className="quick-actions">
          <button>Issue Item</button>
          <button>Manage Stock</button>
          <button>Adjust Stock</button>
        </div>

        <div className="stock-summary">
          <SummaryCard label="Total Stock Items" value="50" type="total" />
          <SummaryCard label="Items Issued" value="35" type="issued" />
          <SummaryCard label="Items Returned" value="20" type="returned" />
        </div>

        <StockTable items={stockItems} />
      </main>
    </div>
  );
}
