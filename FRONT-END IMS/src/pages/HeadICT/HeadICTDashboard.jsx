import React, { useState, useEffect } from 'react';
import './HeadICTDashboard.css';

const Dashboard = () => {
  const [isMobile, setIsMobile] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const data = [
    { label1: 2, label2: 4 },
    { label1: 3, label2: 6 },
    { label1: 5, label2: 9 },
  ];

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (!mobile) {
        setSidebarOpen(true);
      } else {
        setSidebarOpen(false);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
    
    // Toggle body scroll prevention
    if (isMobile) {
      document.body.style.overflow = sidebarOpen ? 'auto' : 'hidden';
    }
  };

  const navItems = [
    { icon: '🏠', label: 'Home' },
    { icon: '📊', label: 'Summary' },
    { icon: '🛡️', label: 'Audit Logs' },
    { icon: '📋', label: 'Reports' },
    { icon: '👥', label: 'Users' },
  ];

  const topLinks = ['Reports', 'Audit Logs', 'Users'];

  const stats = [
    { title: 'Completed Audits', value: 15, isGreen: true },
    { title: 'Pending Audits', value: 5 },
    { title: 'Issues Found', value: 0 },
  ];

  return (
    <div className={`dashboard ${sidebarOpen && isMobile ? 'sidebar-open' : ''}`}>
      {/* Mobile Header */}
      {isMobile && (
        <header className="mobile-header">
          <button className="hamburger" onClick={toggleSidebar}>
            <div className={`hamburger-line ${sidebarOpen ? 'open' : ''}`} />
            <div className={`hamburger-line ${sidebarOpen ? 'open' : ''}`} />
            <div className={`hamburger-line ${sidebarOpen ? 'open' : ''}`} />
          </button>
          <h1>Hello Brian!!</h1>
        </header>
      )}

      {/* Overlay */}
      {isMobile && (
        <div 
          className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`}
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="profile">
          <div className="avatar">B</div>
          <div className="profile-info">
            <div className="name">Brian</div>
            <div className="email">brian@gmail.com</div>
          </div>
        </div>
        
        <nav>
          <ul className="nav-menu">
            {navItems.map((item, index) => (
              <li 
                key={index} 
                className={`nav-item ${index === 0 ? 'active' : ''}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span>{item.label}</span>
              </li>
            ))}
          </ul>
        </nav>
        
        <div className="footer">
          <button className="logout-btn">
            <span>🚪</span> Logout
          </button>
          <p className="authority">ICT Authority</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className={`main ${!sidebarOpen ? 'expanded' : ''}`}>
        {!isMobile && <h1>Hello Brian!!</h1>}
        
        <div className="top-links">
          {topLinks.map((link, index) => (
            <div key={index} className="card-link">
              {link}
            </div>
          ))}
        </div>

        <div className="stats">
          {stats.map((stat, index) => (
            <div 
              key={index} 
              className={`card ${stat.isGreen ? 'green' : ''}`}
            >
              <h4 className="card-title">{stat.title}</h4>
              <p className="big-number">{stat.value}</p>
            </div>
          ))}
        </div>

        <div className="chart-container">
          <div className="legend">
            <div className="legend-item">
              <span className="dot red"></span>
              <span>Label 1</span>
            </div>
            <div className="legend-item">
              <span className="dot green"></span>
              <span>Label 2</span>
            </div>
          </div>
          
          <div className="bars-container">
            {data.map((d, index) => (
              <div key={index} className="bar-group">
                <div 
                  className="bar red" 
                  style={{ height: `${d.label1 * 20}px` }}
                ></div>
                <div 
                  className="bar green" 
                  style={{ height: `${d.label2 * 20}px` }}
                ></div>
                <div className="bar-label">{`Q${index + 1}`}</div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;