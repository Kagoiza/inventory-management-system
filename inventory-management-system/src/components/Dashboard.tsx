
import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import StatsCards from './StatsCards';
import RequestsTable from './RequestsTable';
import { useToast } from '@/hooks/use-toast';

const Dashboard = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const { toast } = useToast();

  const [requests, setRequests] = useState([
    {
      id: 1,
      type: 'Laptop',
      status: 'Approved',
      date: 'May 15, 2025',
      statusColor: 'bg-green-100 text-green-800',
      category: 'Hardware',
      description: 'Dell Latitude 5520 for development work',
      justification: 'Current laptop is outdated and affecting productivity',
      urgency: 'medium'
    },
    {
      id: 2,
      type: 'Desktop',
      status: 'Denied',
      date: 'Apr 30, 2025',
      statusColor: 'bg-red-100 text-red-800',
      category: 'Hardware',
      description: 'High-performance desktop for video editing',
      justification: 'Need more processing power for multimedia projects',
      urgency: 'low'
    },
    {
      id: 3,
      type: 'Office chair',
      status: 'Pending',
      date: 'Apr 3, 2025',
      statusColor: 'bg-yellow-100 text-yellow-800',
      category: 'Furniture',
      description: 'Ergonomic office chair with lumbar support',
      justification: 'Current chair is causing back pain',
      urgency: 'high'
    },
    {
      id: 4,
      type: 'Office desk',
      status: 'Pending',
      date: 'Feb 25, 2025',
      statusColor: 'bg-yellow-100 text-yellow-800',
      category: 'Furniture',
      description: 'Standing desk with adjustable height',
      justification: 'Promote healthier work habits',
      urgency: 'medium'
    },
    {
      id: 5,
      type: 'Router',
      status: 'Open',
      date: 'Feb 22, 2024',
      statusColor: 'bg-blue-100 text-blue-800',
      category: 'Network',
      description: 'Wi-Fi 6 router for conference room',
      justification: 'Current router has poor coverage',
      urgency: 'urgent'
    }
  ]);

  const handleNewRequest = (newRequest: any) => {
    setRequests(prev => [newRequest, ...prev]);
  };

  const handleStatusChange = (id: number, newStatus: string) => {
    setRequests(prev => 
      prev.map(request => 
        request.id === id 
          ? { 
              ...request, 
              status: newStatus,
              statusColor: getStatusColor(newStatus)
            }
          : request
      )
    );
    
    toast({
      title: "Status Updated",
      description: `Request #${id} has been ${newStatus.toLowerCase()}`,
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Approved': return 'bg-green-100 text-green-800';
      case 'Denied': return 'bg-red-100 text-red-800';
      case 'Pending': return 'bg-yellow-100 text-yellow-800';
      case 'Open': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar 
        isCollapsed={isSidebarCollapsed} 
        setIsCollapsed={setIsSidebarCollapsed}
        onNewRequest={handleNewRequest}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header isAdmin={isAdmin} onAdminToggle={setIsAdmin} />
        
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            <StatsCards requests={requests} />
            <RequestsTable 
              requests={requests}
              onStatusChange={handleStatusChange}
              isAdmin={isAdmin}
            />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
