import React from 'react';
import logo from '../assets/icta-logo.png';

const Sidebar = () => (
  <div className="w-60 h-screen fixed top-0 left-0 bg-white text-ictaDark flex flex-col justify-between p-6 border-r shadow z-10">
    <div>
      {/* Logo */}
      <div className="flex items-center space-x-2 mb-8">
        <img src={logo} alt="ICTA" className="h-8" />
      </div>

      {/* Nav */}
      <ul className="space-y-4 text-sm font-medium">
        <li className="hover:text-ictaRed cursor-pointer">🏠 Home</li>
        <li className="hover:text-ictaRed cursor-pointer">📊 Summary</li>
        <li className="hover:text-ictaRed cursor-pointer">🛡 Audit Logs</li>
        <li className="hover:text-ictaRed cursor-pointer">📄 Reports</li>
        <li className="hover:text-ictaRed cursor-pointer">👥 Users</li>
      </ul>
    </div>

    {/* Logout + Footer */}
    <div className="text-sm text-center">
      <button
        className="text-red-600 hover:text-red-800 mt-4 font-semibold"
        onClick={() => {
          localStorage.clear();
          window.location.href = "/login.html";
        }}
      >
        🚪 Logout
      </button>
      <div className="text-xs text-gray-500 mt-4">
        © {new Date().getFullYear()} ICTA
      </div>
    </div>
  </div>
);

export default Sidebar;
