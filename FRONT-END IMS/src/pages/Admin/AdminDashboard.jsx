// src/pages/AdminDashboard.jsx

import React from "react";
import {
  FaHome,
  FaChartBar,
  FaShieldAlt,
  FaFileAlt,
  FaUsers,
  FaSignOutAlt,
} from "react-icons/fa";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import "./AdminDashboard.css";

const AdminDashboard = () => {
  const chartData = [
    { name: "Mon", Issued: 40, Returned: 20 },
    { name: "Tue", Issued: 30, Returned: 20 },
    { name: "Wed", Issued: 20, Returned: 15 },
    { name: "Thu", Issued: 28, Returned: 25 },
    { name: "Fri", Issued: 18, Returned: 10 },
  ];

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="sidebar-top">
          <h2>ICT Authority</h2>
          <ul>
            <li><FaHome /> Home</li>
            <li><FaChartBar /> Summary</li>
            <li><FaShieldAlt /> Audit Logs</li>
            <li><FaFileAlt /> Reports</li>
            <li><FaUsers /> Users</li>
          </ul>
        </div>
        <div className="sidebar-bottom">
          <button className="logout"><FaSignOutAlt /> Logout</button>
          <footer>© 2025 ICTA</footer>
        </div>
      </aside>

      <main className="main-content">
        <header className="main-header">
          <h1>Hello Brian</h1>
        </header>

        <div className="stat-cards">
          <div className="card blue"><h4>Total Stock</h4><p>3,000</p></div>
          <div className="card red"><h4>Low Stock</h4><p>30</p></div>
          <div className="card white"><h4>Issued Today</h4><p>75</p></div>
          <div className="card yellow"><h4>Pending Returns</h4><p>12</p></div>
        </div>

        <div className="chart-section">
          <h3>Stock Movement (This Week)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="Issued" fill="#388e3c" />
              <Bar dataKey="Returned" fill="#c62828" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;

