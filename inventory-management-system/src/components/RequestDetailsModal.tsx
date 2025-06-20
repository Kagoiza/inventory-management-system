
import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';

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

interface RequestDetailsModalProps {
  request: Request | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onStatusChange: (id: number, status: string) => void;
  isAdmin?: boolean;
}

const RequestDetailsModal = ({ 
  request, 
  open, 
  onOpenChange, 
  onStatusChange, 
  isAdmin = false 
}: RequestDetailsModalProps) => {
  const { toast } = useToast();

  if (!request) return null;

  const handleStatusChange = (newStatus: string) => {
    onStatusChange(request.id, newStatus);
    onOpenChange(false);
    
    toast({
      title: "Status Updated",
      description: `Request has been ${newStatus.toLowerCase()}`,
    });
  };

  const getUrgencyColor = (urgency?: string) => {
    switch (urgency) {
      case 'urgent': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-blue-100 text-blue-800';
      case 'low': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Request Details - #{request.id}</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label className="text-sm font-medium text-gray-500">Item Type</Label>
              <p className="text-lg font-semibold">{request.type}</p>
            </div>
            <div>
              <Label className="text-sm font-medium text-gray-500">Status</Label>
              <div className="mt-1">
                <Badge className={request.statusColor}>
                  {request.status}
                </Badge>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label className="text-sm font-medium text-gray-500">Application Date</Label>
              <p>{request.date}</p>
            </div>
            {request.urgency && (
              <div>
                <Label className="text-sm font-medium text-gray-500">Urgency</Label>
                <div className="mt-1">
                  <Badge className={getUrgencyColor(request.urgency)}>
                    {request.urgency}
                  </Badge>
                </div>
              </div>
            )}
          </div>

          {request.category && (
            <div>
              <Label className="text-sm font-medium text-gray-500">Category</Label>
              <p>{request.category}</p>
            </div>
          )}

          {request.description && (
            <div>
              <Label className="text-sm font-medium text-gray-500">Description</Label>
              <p className="text-gray-700">{request.description}</p>
            </div>
          )}

          {request.justification && (
            <div>
              <Label className="text-sm font-medium text-gray-500">Business Justification</Label>
              <p className="text-gray-700">{request.justification}</p>
            </div>
          )}

          {isAdmin && request.status === 'Pending' && (
            <div className="flex space-x-2 pt-4 border-t">
              <Button 
                onClick={() => handleStatusChange('Approved')} 
                className="bg-green-600 hover:bg-green-700"
              >
                Approve
              </Button>
              <Button 
                onClick={() => handleStatusChange('Denied')} 
                variant="destructive"
              >
                Deny
              </Button>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default RequestDetailsModal;
