import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";
import StatusCards from "./StatusCards";
import AuditChart from "./AuditChart";

// Placeholder components for routing (to be replaced later)
const HomePage: React.FC = () => (
  <div>
    <Header />
    <div className="quick-links">
      <button>Reports</button>
      <button>Audit Logs</button>
      <button>Users</button>
    </div>
    <StatusCards />
    <AuditChart />
  </div>
);

const LoginPage: React.FC = () => <h2>Login Page (Coming Soon)</h2>;
const SummaryPage: React.FC = () => <h2>Summary Page (Coming Soon)</h2>;
const AuditLogsPage: React.FC = () => <h2>Audit Logs Page (Coming Soon)</h2>;
const ReportsPage: React.FC = () => <h2>Reports Page (Coming Soon)</h2>;
const UsersPage: React.FC = () => <h2>Users Page (Coming Soon)</h2>;

const App: React.FC = () => {
  return (
    <Router>
      <div className="dashboard">
        <Sidebar />
        <main className="main">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/summary" element={<SummaryPage />} />
            <Route path="/audit-logs" element={<AuditLogsPage />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/users" element={<UsersPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
