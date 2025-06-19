import logo from '../assets/icta-logo.png';

const Sidebar = () => (
  <div className="w-60 h-screen bg-ictaRed text-white fixed p-6 flex flex-col justify-between">
    <div>
      <div className="mb-8">
        <img src={logo} alt="ICTA" className="h-10 mx-auto" />
      </div>
      <ul className="space-y-4">
        <li>🏠 Home</li>
        <li>📊 Summary</li>
        <li>🛡 Audit Logs</li>
        <li>📄 Reports</li>
        <li>👥 Users</li>
      </ul>
    </div>
    <div className="mt-6 text-center text-sm">
      © {new Date().getFullYear()} ICT Authority
    </div>
  </div>
);

export default Sidebar;
