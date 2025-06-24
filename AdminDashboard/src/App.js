import React from 'react';
import Sidebar from './components/Sidebar';
import AdminDashboard from './components/AdminDashboard';

function App() {
  return (
    <div className="flex">
      <Sidebar />
      <div className="ml-60 p-6 bg-ictaGray min-h-screen w-full">
        <AdminDashboard />
      </div>
    </div>
  );
}

export default App;
