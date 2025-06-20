
import React from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface AdminToggleProps {
  isAdmin: boolean;
  onToggle: (isAdmin: boolean) => void;
}

const AdminToggle = ({ isAdmin, onToggle }: AdminToggleProps) => {
  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-gray-600">View as:</span>
      <Button
        variant={!isAdmin ? "default" : "outline"}
        size="sm"
        onClick={() => onToggle(false)}
      >
        User
      </Button>
      <Button
        variant={isAdmin ? "default" : "outline"}
        size="sm"
        onClick={() => onToggle(true)}
      >
        Admin
      </Button>
      {isAdmin && (
        <Badge variant="secondary" className="ml-2">
          Admin Mode
        </Badge>
      )}
    </div>
  );
};

export default AdminToggle;
