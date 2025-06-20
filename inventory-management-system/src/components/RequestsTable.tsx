
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import RequestDetailsModal from './RequestDetailsModal';
import { Search } from 'lucide-react';

interface Request {
  id: number;
  type: string;
  status: string;
  date: string;
  statusColor: string;
  category?: string;
  description?: string;
  justification?: string;
  urgency?: string;
}

interface RequestsTableProps {
  requests: Request[];
  onStatusChange: (id: number, status: string) => void;
  isAdmin?: boolean;
}

const RequestsTable = ({ requests, onStatusChange, isAdmin = false }: RequestsTableProps) => {
  const [selectedRequest, setSelectedRequest] = useState<Request | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const filteredRequests = requests.filter(request => {
    const matchesSearch = request.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.id.toString().includes(searchTerm);
    const matchesStatus = statusFilter === 'all' || request.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleViewRequest = (request: Request) => {
    setSelectedRequest(request);
    setModalOpen(true);
  };

  return (
    <>
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gray-100 rounded-lg">
              <div className="w-5 h-5 bg-gray-400 rounded"></div>
            </div>
            <h2 className="text-xl font-semibold text-gray-900">Request Summary</h2>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search by item type or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-full sm:w-48">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="Pending">Pending</SelectItem>
              <SelectItem value="Approved">Approved</SelectItem>
              <SelectItem value="Denied">Denied</SelectItem>
              <SelectItem value="Open">Open</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-gray-500">Item ID</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Application Date</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredRequests.map((request) => (
                <tr key={request.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4 text-gray-900">{request.id}</td>
                  <td className="py-4 px-4 text-gray-900">{request.type}</td>
                  <td className="py-4 px-4">
                    <Badge className={request.statusColor}>
                      {request.status}
                    </Badge>
                  </td>
                  <td className="py-4 px-4 text-gray-600">{request.date}</td>
                  <td className="py-4 px-4">
                    <div className="flex space-x-2">
                      <Button 
                        variant="link" 
                        className="text-blue-600 p-0"
                        onClick={() => handleViewRequest(request)}
                      >
                        View
                      </Button>
                      {isAdmin && request.status === 'Pending' && (
                        <>
                          <Button 
                            variant="link" 
                            className="text-green-600 p-0"
                            onClick={() => onStatusChange(request.id, 'Approved')}
                          >
                            Approve
                          </Button>
                          <Button 
                            variant="link" 
                            className="text-red-600 p-0"
                            onClick={() => onStatusChange(request.id, 'Denied')}
                          >
                            Deny
                          </Button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredRequests.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No requests found matching your criteria.
          </div>
        )}
      </Card>

      <RequestDetailsModal
        request={selectedRequest}
        open={modalOpen}
        onOpenChange={setModalOpen}
        onStatusChange={onStatusChange}
        isAdmin={isAdmin}
      />
    </>
  );
};

export default RequestsTable;
