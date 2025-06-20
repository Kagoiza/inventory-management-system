import React from 'react';
import SummaryCard from './SummaryCard';
import ChartSection from './ChartSection';
import StockAlertTable from './StockAlertTable';
import ReportsSection from './ReportsSection';
import logo from '../assets/icta-logo.png';

const Sidebar = () => (
  <div className="w-60 h-screen fixed top-0 left-0 bg-ictaDark text-white flex flex-col justify-between p-6 z-10">
    <div>
      <div className="flex items-center space-x-2 mb-8">
        <img src={logo} alt="ICTA" className="h-8" />
        <span className="text-lg font-semibold">ICT Authority</span>
      </div>
      <ul className="space-y-4 text-sm">
        <li className="hover:text-ictaGreen cursor-pointer">🏠 Home</li>
        <li className="hover:text-ictaGreen cursor-pointer">📊 Summary</li>
        <li className="hover:text-ictaGreen cursor-pointer">🛡 Audit Logs</li>
        <li className="hover:text-ictaGreen cursor-pointer">📄 Reports</li>
        <li className="hover:text-ictaGreen cursor-pointer">👥 Users</li>
      </ul>
    </div>
    <div className="text-sm text-center">
      © {new Date().getFullYear()} ICTA
    </div>
  </div>
);


const AdminDashboard = () => {
  return (
    <div className="flex">
      <Sidebar />
      <div className="ml-60 p-6 bg-ictaGray min-h-screen w-full">
        <div className="flex items-center space-x-4 mb-6">
          <img src={logo} alt="ICTA logo" className="h-12" />
          <h1 className="text-3xl font-bold text-ictaDark">ICTA Admin Dashboard</h1>

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
    </div>
  );
};

export default AdminDashboard;
