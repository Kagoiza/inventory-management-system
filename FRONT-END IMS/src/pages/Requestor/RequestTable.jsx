import React from 'react';
import './RequestTable.css';

const RequestTable = () => {
  const data = [
    { id: 1, type: 'Laptop', status: 'Approved', date: 'May 15, 2025' },
    { id: 2, type: 'Desktop', status: 'Denied', date: 'Apr 30, 2025' },
    { id: 3, type: 'Office chair', status: 'Pending', date: 'Apr 3, 2025' },
    { id: 4, type: 'Office desk', status: 'Pending', date: 'Feb 25, 2025' },
    { id: 5, type: 'Router', status: 'Open', date: 'Feb 22, 2024' },
  ];

  return (
    <table className="request-table">
      <thead>
        <tr>
          <th>Item ID</th>
          <th>Type</th>
          <th>Status</th>
          <th>Application Date</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.type}</td>
            <td><span className={`status ${item.status.toLowerCase()}`}>{item.status}</span></td>
            <td>{item.date}</td>
            <td><a href="#">View</a></td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default RequestTable;
