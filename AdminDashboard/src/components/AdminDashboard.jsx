import React from 'react';
import SummaryCard from './SummaryCard';
import ChartSection from './ChartSection';
import StockAlertTable from './StockAlertTable';
import ReportsSection from './ReportsSection';
import logo from '../assets/icta-logo.png';

const AdminDashboard = () => {
  return (
    <div>
      <div className="flex items-center space-x-4 mb-6">
        <img src={logo} alt="ICTA logo" className="h-12" />
        <h1 className="text-3xl font-bold text-ictaDark">Admin Dashboard</h1>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <SummaryCard title="Total Stock" value="3,000" color="bg-blue-600" />
        <SummaryCard title="Low Stock" value="30" color="bg-red-500" />
        <SummaryCard title="Issued Today" value="75" color="bg-green-600" />
        <SummaryCard title="Pending Returns" value="12" color="bg-yellow-500" />
      </div>

      <ChartSection />
      <StockAlertTable />
      <ReportsSection />
    </div>
  );
};

export default AdminDashboard;
