import React from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DashboardCards from './components/DashboardCards';
import StockTable from './components/StockTable';

function App() {
  return (
    <div className="app">
      <Sidebar />
      <main>
        <Header />
        <DashboardCards />
        <StockTable />
      </main>
    </div>
  );
}

export default App;

