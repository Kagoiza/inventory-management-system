import React from 'react';
import './StockTable.css';

const data = [
  { id: 1, type: 'Laptop', category: 'ICT Hardware', status: 'Approve', date: 'May 15, 2025' },
  { id: 2, type: 'Desktop', category: 'ICT Hardware', status: 'Not Approved', date: 'Apr 30, 2025' },
  { id: 3, type: 'Office chair', category: 'ICT Furniture', status: 'Approve', date: 'Apr 3, 2025' },
  { id: 4, type: 'Office desk', category: 'ICT Furniture', status: 'Not Approved', date: 'Mar 25, 2025' },
  { id: 5, type: 'Router', category: 'Networking Devices', status: 'Approve', date: 'Mar 22, 2025' },
];

const StockTable = () => {
  return (
    <div className="table-container">
      <div className="table-header">
        <h3>Stock Summary</h3>
        <div>
          <button>Filter</button>
          <button className="export">Export</button>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Item Id</th>
            <th>Type</th>
            <th>Category</th>
            <th>Status</th>
            <th>Date Returned</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.type}</td>
              <td>{item.category}</td>
              <td>
  <span className={item.status === 'Approve' ? 'status-approved' : 'status-not-approved'}>
    {item.status}
  </span>
</td>
              <td>{item.date}</td>
              <td><button type="button" className="view-btn">View</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StockTable;
