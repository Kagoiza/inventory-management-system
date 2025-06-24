import React from 'react';
import './StockTable.css';

export default function StockTable({ items }) {
  return (
    <div className="table-section">
      <div className="table-controls">
        <button>Filter</button>
        <button className="export">Export</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Item Id</th>
            <th>Type</th>
            <th>Status</th>
            <th>Expiration Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.type}</td>
              <td><span className="status approve">{item.status}</span></td>
              <td>{item.expiration}</td>
              <td><a href="#view">View</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
