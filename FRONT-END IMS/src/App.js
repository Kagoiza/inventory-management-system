import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import AdminDashboard from './pages/Admin/AdminDashboard';
import RequestorDashboard from './pages/Requestor/RequestorDashboard';
import StoreClerkDashboard from './pages/StoreClerk/StoreClerkDashboard';
import HeadICTDashboard from './pages/HeadICT/HeadICTDashboard';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';

function App() {
  return (
    <Router>
      {/* TEMPORARY NAVIGATION MENU */}
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <Link to="/" style={{ marginRight: '10px' }}>Login</Link>
        <Link to="/register" style={{ marginRight: '10px' }}>Register</Link>
        <Link to="/admin" style={{ marginRight: '10px' }}>Admin</Link>
        <Link to="/requestor" style={{ marginRight: '10px' }}>Requestor</Link>
        <Link to="/storeclerk" style={{ marginRight: '10px' }}>Store Clerk</Link>
        <Link to="/headict">Head ICT</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/requestor" element={<RequestorDashboard />} />
        <Route path="/storeclerk" element={<StoreClerkDashboard />} />
        <Route path="/headict" element={<HeadICTDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
