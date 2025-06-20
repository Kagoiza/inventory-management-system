import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  FaBars, 
  FaHome, 
  FaChartBar, 
  FaClipboardList, 
  FaFileAlt, 
  FaUsers, 
  FaSignOutAlt 
} from 'react-icons/fa';

const Sidebar: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      {/* Toggle Button */}
      <div className="toggle-button" onClick={toggleSidebar}>
        <FaBars />
      </div>

      {/* User Info */}
      {!collapsed && (
        <div className="user-info">
          <div className="avatar">A</div>
          <div>
            <p>A</p>
            <p>abbiekaggz@gmail.com</p>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav>
        <Link to="/"><FaHome /> {!collapsed && 'Home'}</Link>
        <Link to="/summary"><FaChartBar /> {!collapsed && 'Summary'}</Link>
        <Link to="/audit-logs"><FaClipboardList /> {!collapsed && 'Audit Logs'}</Link>
        <Link to="/reports"><FaFileAlt /> {!collapsed && 'Reports'}</Link>
        <Link to="/users"><FaUsers /> {!collapsed && 'Users'}</Link>
       <Link to="/login" className="logout"><FaSignOutAlt /> {!collapsed && 'Logout'}</Link>
        {!collapsed && <Link to="#" className="footer-link">ICT Authority</Link>}
      </nav>
    </aside>
  );
};

export default Sidebar;
