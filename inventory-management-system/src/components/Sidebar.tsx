
import React from 'react';
import { Home, FileText, BarChart3, LogOut, Menu, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import RequestModal from './RequestModal';

interface SidebarProps {
  isCollapsed: boolean;
  setIsCollapsed: (collapsed: boolean) => void;
  onNewRequest: (request: any) => void;
}

const Sidebar = ({ isCollapsed, setIsCollapsed, onNewRequest }: SidebarProps) => {
  const menuItems = [
    { icon: Home, label: 'Home', active: true },
    { icon: FileText, label: 'Request Item', active: false },
    { icon: BarChart3, label: 'Request Summary', active: false },
  ];

  return (
    <div className={`bg-white h-screen border-r border-gray-200 transition-all duration-300 ${isCollapsed ? 'w-16' : 'w-64'}`}>
      <div className="p-4">
        <div className="flex items-center justify-between mb-8">
          {!isCollapsed && (
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold">S</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Sarah</h3>
                <p className="text-sm text-gray-500">sarah@corp.com</p>
              </div>
            </div>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-2"
          >
            <Menu className="h-4 w-4" />
          </Button>
        </div>

        {/* Quick Request Button */}
        <div className="mb-6">
          <RequestModal onSubmit={onNewRequest}>
            <Button className="w-full bg-green-500 hover:bg-green-600 text-white">
              <Plus className="h-4 w-4 mr-2" />
              {!isCollapsed && "New Request"}
            </Button>
          </RequestModal>
        </div>

        <nav className="space-y-2">
          {menuItems.map((item, index) => (
            <button
              key={index}
              className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                item.active 
                  ? 'bg-green-50 text-green-700 border-r-2 border-green-500' 
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <item.icon className="h-5 w-5" />
              {!isCollapsed && <span className="font-medium">{item.label}</span>}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-8 left-4 right-4">
          <div className="mb-4">
            {!isCollapsed && (
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-xs font-semibold text-blue-600">ICT</span>
                </div>
                <span className="text-sm text-gray-600">ICT Authority</span>
              </div>
            )}
          </div>
          <button className="w-full flex items-center space-x-3 px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
            <LogOut className="h-5 w-5" />
            {!isCollapsed && <span className="font-medium">Logout</span>}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
